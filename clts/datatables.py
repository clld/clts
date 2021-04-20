from sqlalchemy.orm import joinedload
from purl import URL

from clld.web.datatables.base import Col, LinkCol, DetailsRowLinkCol, DataTable
from clld.web.datatables.contribution import Contributions
from clld.web.datatables.contributor import Contributors, NameCol, ContributionsCol
from clld.web.datatables.parameter import Parameters
from clld.web.datatables.value import Values
from clld.web.util.helpers import linked_references, external_link
from clld.web.util.htmllib import HTML
from clld.db.models.common import Value, ValueSet, Parameter, Contribution, ContributionContributor
from clld.db.util import get_distinct_values

from clts.models import SoundSegment, Feature, Transcription, Datatype

LEGEND = {
    '#c86464': ("V", "all vowels and diphthongs", "a e i o u"),
    '#c89664': ("K", "affricates, uvulars, and velars", "k g t ts"),
    '#c8c864': ("P", "bilabials and labiodentals", "p f pf"),
    '#96c864': ("H", "glottals sounds", "h ʔ"),
    '#64c864': ("J", "palatal glides", "j, ɥ, ɰ"),
    '#64c896': ("M", "bilabial nasals", "m, ɱ"),
    '#64c8c8': ("N", "nasals", "n, ŋ"),
    '#6496c8': ("S", "sibilant fricatives", "s z ʃ ʒ"),
    '#6464c8': ("R", "r-sounds and l-sounds", "r l"),
    '#9664c8': ("T", "dental and alveolar stops", "t d"),
    '#c864c8': ("W", "labial glide", "w v"),
    '#c86496': ("1", "any tone", "¹¹, ²²"),
    '#bbbbbb': ("-", "markers", " +"),
}
CLS_TO_COLOR = {v[0]: k for k, v in LEGEND.items()}


class Authors(Contributors):
    def base_query(self, query):
        return query.join(ContributionContributor)

    def col_defs(self):
        return [
            NameCol(self, 'name'),
            ContributionsCol(self, ''),
        ]


class DescriptionLinkCol(LinkCol):
    def get_attrs(self, item):
        return {'label': item.description}


class ColorCol(Col):
    __kw__ = dict(
        sDescription='Sound classes according to Dolgopolsky (1964).',
        choices=[(k, '{0}: {1}'.format(*v)) for k, v in LEGEND.items()])

    def search(self, qs):
        return SoundSegment.color == CLS_TO_COLOR.get(qs, qs)

    def format(self, item):
        return HTML.div(HTML.strong(LEGEND[item.color][0]),
                        style="background-color: {}; text-align: center;".format(item.color))


class SoundSegments(Parameters):
    def col_defs(self):
        return [
            LinkCol(self, 'name', sTitle='Grapheme'),
            DescriptionLinkCol(self, 'description', sTitle='Name'),
            ColorCol(self, 'class'),
            Col(self, 'unicode', sTitle="Unicode", model_col=SoundSegment.unicode),
            Col(self, 'representation', sTitle='Representation', model_col=SoundSegment.representation)
        ]


class URLCol(Col):
    __kw__ = dict(bSortable=False, bSearchable=False)

    def format(self, item):
        if item.url:
            return external_link(item.url, label=URL(item.url).host())


class SoundSegmentGraphemeCol(LinkCol):
    def get_obj(self, item):
        return item.valueset.parameter


class SoundSegmentNameCol(SoundSegmentGraphemeCol):
    def get_attrs(self, item):
        return {'label': item.valueset.parameter.description}


class AudioCol(Col):
    __kw__ = dict(bSearchable=False, bSortable=False)

    def format(self, item):
        if item.audio:
            return HTML.audio(
                HTML.source(src=item.audio, type="audio/mpeg"),
                controls="controls"
            )
        return ''


class ImageCol(Col):
    __kw__ = dict(bSearchable=False, bSortable=False)

    def format(self, item):
        if item.image:
            return HTML.img(src=item.image, height=20, type="audio/mpeg")
        return ''


class Graphemes(Values):
    def base_query(self, query):
        if self.parameter:
            query = query \
                .join(ValueSet)\
                .join(Contribution)\
                .options(joinedload(Value.valueset).joinedload(ValueSet.contribution))
            return query.filter(ValueSet.parameter_pk == self.parameter.pk).distinct()

        if self.contribution:
            query = query \
                .join(ValueSet) \
                .join(ValueSet.parameter) \
                .options(joinedload(Value.valueset).joinedload(ValueSet.parameter))
            return query.filter(ValueSet.contribution_pk == self.contribution.pk)

        return query \
            .join(ValueSet) \
            .join(Contribution) \
            .join(ValueSet.parameter) \
            .options(
                joinedload(Value.valueset).joinedload(ValueSet.contribution),
                joinedload(Value.valueset, ValueSet.parameter)
            )

    def col_defs(self):
        res = [Col(self, 'name', sTitle='Grapheme')]
        if not self.parameter:
            res.extend([
                SoundSegmentGraphemeCol(self, 'bipa_grapheme', model_col=Parameter.name, sTitle="BIPA Grapheme"),
                SoundSegmentNameCol(self, 'name', model_col=Parameter.description),
            ])

        if not self.contribution:
            res.extend([
                LinkCol(
                    self,
                    'transcription_data',
                    get_object=lambda v: v.valueset.contribution,
                    sTitle="Dataset",
                    model_col=Contribution.id),
                DatatypeCol(
                    self,
                    'type',
                    get_object=lambda v: v.valueset.contribution,
                    **({} if self.parameter else {'sFilter': 'transcription system'})),
            ])
        if self.contribution:
            if self.contribution.with_url:
                res.append(URLCol(self, 'url', sTitle="URL"))
            if self.contribution.with_image:
                res.append(ImageCol(self, 'image'))
            if self.contribution.with_audio:
                res.append(AudioCol(self, 'audio'))
        return res

    def get_options(self):
        if self.parameter:
            return {'aaSorting': [[2, 'asc'], [1, 'asc']]}
        return {}


class RefsCol(Col):
    __kw__ = {'bSortable': False, 'bSearchable': False}

    def format(self, item):
        return linked_references(self.dt.req, item)


class DatatypeCol(Col):
    def __init__(self, dt, name, **kw):
        kw['choices'] = get_distinct_values(Transcription.datatype)
        super(DatatypeCol, self).__init__(dt, name, **kw)

    def search(self, qs):
        return Transcription.datatype == Datatype.from_string(qs)

    def order(self):
        return Transcription.datatype

    def format(self, item):
        item = self.get_obj(item)
        return item.datatype.value


class Datasets(Contributions):
    def col_defs(self):
        return [
            DetailsRowLinkCol(self, '#', button_text='info'),
            LinkCol(self, 'name'),
            DatatypeCol(self, 'type'),
            Col(self, 'graphemes', model_col=Transcription.items),
            #Col(self, 'description', sTitle='Description', sType='html', format=lambda i: markdown(i.description)),
            RefsCol(self, 'sources'),
        ]

    def get_options(self):
        return {'aaSorting': [[2, 'asc'], [1, 'asc']]}


class Features(DataTable):
    def col_defs(self):
        return [
            LinkCol(self, 'name'),
            Col(self, 'sound_type', model_col=Feature.sound_type, choices=get_distinct_values(Feature.sound_type)),
            Col(self, 'feature', model_col=Feature.feature, choices=get_distinct_values(Feature.feature)),
            Col(self, 'value', sTitle='Value', model_col=Feature.value),
            Col(self, 'sounds', sTitle='# sounds', model_col=Feature.count_sounds),
        ]


def includeme(config):
    config.register_datatable('parameters', SoundSegments)
    config.register_datatable('values', Graphemes)
    config.register_datatable('contributions', Datasets)
    config.register_datatable('features', Features)

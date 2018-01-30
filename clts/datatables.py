from __future__ import unicode_literals

from sqlalchemy.orm import aliased, joinedload, joinedload_all
from purl import URL

from clld.web.datatables.base import Col, LinkCol, IdCol, DetailsRowLinkCol, IntegerIdCol
from clld.web.datatables.contribution import Contributions, ContributorsCol
from clld.web.datatables.contributor import Contributors, NameCol, ContributionsCol
from clld.web.datatables.parameter import Parameters
from clld.web.datatables.value import Values
from clld.web.util.helpers import linked_references, external_link
from clld.db.models.common import (
    Value, Value_data, ValueSet, Parameter, Contribution, ContributionContributor,
    ContributionReference,
)

from clts.models import SoundSegment, Grapheme
from clts.util import markdown


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


class SoundSegments(Parameters):
    def col_defs(self):
        return [
            LinkCol(self, 'name', sTitle='Grapheme'),
            DescriptionLinkCol(self, 'description', sTitle='Name'),
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


class Graphemes(Values):
    def base_query(self, query):
        if self.parameter:
            query = query.join(ValueSet).options(joinedload_all(Value.valueset))
            return query.filter(ValueSet.parameter_pk == self.parameter.pk)

        query = query\
            .join(ValueSet)\
            .join(ValueSet.parameter)\
            .options(joinedload_all(Value.valueset, ValueSet.parameter))

        if self.contribution:
            return query.filter(ValueSet.contribution_pk == self.contribution.pk)

        return query

    def col_defs(self):
        res = [Col(self, 'name', sTitle='Grapheme')]
        if not self.parameter:
            res.extend([
                SoundSegmentGraphemeCol(self, 'bipa_grapheme', model_col=Parameter.name, sTitle="BIPA Grapheme"),
                SoundSegmentNameCol(self, 'name', model_col=Parameter.description),
                Col(self, 'frequency', sTitle='Frequency'),
            ])
        if not self.contribution:
            res.append(
                LinkCol(self, 'transcription_data', get_object=lambda v:
                    v.valueset.contribution, sTitle="Dataset"))
        res.append(URLCol(self, 'url', sTitle="URL"))
        return res


class RefsCol(Col):
    __kw__ = {'bSortable': False, 'bSearchable': False}

    def format(self, item):
        return linked_references(self.dt.req, item)


class Datasets(Contributions):
    def col_defs(self):
        return [
            LinkCol(self, 'name'),
            Col(self, 'description', sTitle='Description', sType='html', format=lambda i: markdown(i.description)),
            RefsCol(self, 'sources'),
        ]


def includeme(config):
    config.register_datatable('parameters', SoundSegments)
    config.register_datatable('values', Graphemes)
    config.register_datatable('contributions', Datasets)

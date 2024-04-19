from pathlib import Path

from sqlalchemy.orm import joinedload
from clld.cliutil import Data, bibtex2source
from clld.db.meta import DBSession
from clld.db.models import common
from clld.lib.bibtex import Database

from clts import models

from pyclts.api import CLTS
from clldutils.misc import slug
from clldutils.apilib import assert_release

from clts.datatables import LEGEND


def main(args):  # pragma: no cover
    data = Data()
    clts_repos = Path(__file__).parent.parent.parent.parent.resolve() / 'clts-data'
    clts_repos = CLTS(clts_repos)
    print(clts_repos.repos)
    version = assert_release(clts_repos.repos)

    for rec in Database.from_file(args.cldf.bibpath, lowercase=True):
        data.add(common.Source, rec.id, _obj=bibtex2source(rec))

    dataset = common.Dataset(
        id='clts',
        name="CLTS {0}".format(version),
        publisher_name="Max Planck Institute for Evolutionary Anthropology",
        publisher_place="Leipzig",
        publisher_url="http://www.eva.mpg.de",
        license="http://creativecommons.org/licenses/by/4.0/",
        contact='clts@shh.mpg.de',
        domain='clts.clld.org',
        jsondata={
            'license_icon': 'cc-by.png',
            'license_name': 'Creative Commons Attribution 4.0 International License'})
    DBSession.add(dataset)
    for i, name in enumerate([
        'Johann-Mattis List',
        'Cormac Anderson',
        'Tiago Tresoldi',
        'Robert Forkel',
    ]):
        c = common.Contributor(id=slug(name), name=name)
        dataset.editors.append(common.Editor(contributor=c, ord=i))

    for line in args.cldf['data/features.tsv']:
        data.add(
            models.Feature,
            line['ID'],
            id=line['ID'],
            name='{} {}: {}'.format(line['TYPE'], line['FEATURE'], line['VALUE']),
            sound_type=line['TYPE'],
            feature=line['FEATURE'],
            value=line['VALUE'],
        )

    DBSession.add(models.SoundSegment(
        id='NA',
        name='<NA>',
        description='<NA>',
        type='marker',
        generated=True,
        unicode='',
        color='#bbbbbb',
    ))
    for line in args.cldf['data/sounds.tsv']:
        s = data.add(
            models.SoundSegment,
            line['ID'],
            id=line['ID'],
            name=line['GRAPHEME'],
            description=line['NAME'],
            type=line['TYPE'],
            generated=line['GENERATED'],
            unicode=' / '.join(line['UNICODE']),
            color=clts_repos.soundclass('color').resolve_sound(line['GRAPHEME']),
        )
        if s.color == '0':
            s.color = '#bbbbbb'
        assert s.color in LEGEND
    DBSession.flush()

    seen = set()
    for line in args.cldf['data/sounds.tsv']:
        for fid in line['FEATURES']:
            spk, fpk = data['SoundSegment'][line['ID']].pk, data['Feature'][fid].pk
            if (spk, fpk) not in seen:
                DBSession.add(models.SoundSegmentFeature(soundsegment_pk=spk, feature_pk=fpk))
                seen.add((spk, fpk))

    english = data.add(
        common.Language, 'eng',
        id='eng',
        name='English')

    for line in args.cldf['sources/index.tsv']:
        c = data.add(
            models.Transcription,
            line['NAME'],
            id=line['NAME'],
            name=line['NAME'],
            description=line['DESCRIPTION'].replace(':bib:', '/sources/'),
            datatype=getattr(models.Datatype, line['TYPE'])
        )
        for ref in line.get('REFS', []):
            common.ContributionReference(source=data['Source'][ref], contribution=c)

    sound_url_template = args.cldf['data/graphemes.tsv', 'SOUND'].valueUrl
    image_url_template = args.cldf['data/graphemes.tsv', 'IMAGE'].valueUrl

    for line in args.cldf['data/graphemes.tsv']:
        key = line['DATASET'] + ':' + line['NAME'] + ':' + line['GRAPHEME']
        if key not in data['Grapheme']:
            sound_id = line['NAME'].replace(' ', '_')
            vs = data['ValueSet'].get((line['DATASET'], line['NAME']))
            if not vs:
                try:
                    vs = data.add(
                        common.ValueSet,
                        (line['DATASET'], line['NAME']),
                        id=key,
                        description=line['NAME'],
                        language=english,
                        contribution=data['Transcription'][line['DATASET']],
                        parameter=data['SoundSegment'][sound_id]
                    )
                except:
                    print(line)
                    raise
            data.add(
                models.Grapheme,
                key,
                id=key,
                name=line['GRAPHEME'],
                description=line['NAME'],
                url=line['URL'].unsplit() if line['URL'] else None,
                audio=sound_url_template.expand(line) if line['SOUND'] else None,
                image=image_url_template.expand(line) if line['IMAGE'] else None,
                valueset=vs
            )


def prime_cache(args):  # pragma: no cover
    """If data needs to be denormalized for lookup, do that here.
    This procedure should be separate from the db initialization, because
    it will have to be run periodiucally whenever data has been updated.
    """
    q = DBSession.query(models.Transcription) \
        .join(common.ValueSet, common.ValueSet.contribution_pk == models.Transcription.pk) \
        .join(common.Value, common.Value.valueset_pk == common.ValueSet.pk) \
        .join(models.Grapheme, models.Grapheme.pk == common.Value.pk)

    for t in q.filter(models.Grapheme.audio != None):
        t.with_audio = True

    for t in q.filter(models.Grapheme.image != None):
        t.with_image = True

    for t in q.filter(models.Grapheme.url != None):
        t.with_url = True

    for p in DBSession.query(common.Parameter) \
            .options(joinedload(common.Parameter.valuesets).joinedload(common.ValueSet.values)):
        p.representation = sum(len(vs.values) for vs in p.valuesets)

    for p in DBSession.query(models.Feature).options(joinedload(models.Feature.sounds)):
        p.count_sounds = len(p.sounds)

    for p in DBSession.query(common.Contribution)\
            .options(joinedload(common.Contribution.valuesets).joinedload(common.ValueSet.values)):
        p.items = sum(len(vs.values) for vs in p.valuesets)

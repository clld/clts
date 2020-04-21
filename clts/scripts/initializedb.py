import sys
from pathlib import Path

from tqdm import tqdm
from sqlalchemy.orm import joinedload
from clld.scripts.util import initializedb, Data, bibtex2source
from clld.db.meta import DBSession
from clld.db.models import common
from clld.lib.bibtex import Database

from clts import models

from pyclts.api import CLTS
from csvw.dsv import reader
from clldutils.misc import slug
from clldutils.apilib import assert_release


def iterrows(clts, what):
    comps = []
    if what == 'index':
        comps = ['..', 'sources']
    comps.append('{0}.tsv'.format(what))
    return tqdm(
        reader(clts.data_path(*comps), delimiter='\t', namedtuples=True),
        desc='loading {0}'.format(what))


def main(args):  # pragma: no cover
    data = Data()
    clts = CLTS(Path(__file__).parent.parent.parent.resolve() / '..' / '..' / 'cldf' / 'clts')
    version = assert_release(clts.repos)

    for rec in Database.from_file(clts.data_path('references.bib'), lowercase=False):
        data.add(common.Source, rec.id, _obj=bibtex2source(rec))
    
    dataset = common.Dataset(
        id='clts',
        name="CLTS {0}".format(version),
        publisher_name="Max Planck Institute for the Science of Human History",
        publisher_place="Jena",
        publisher_url="http://www.shh.mpg.de",
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
        'Christoph Rzymski',
        'Simon Greenhill',
        'Robert Forkel',
    ]):
        c = common.Contributor(id=slug(name), name=name)
        dataset.editors.append(common.Editor(contributor=c, ord=i))

    for line in iterrows(clts, 'sounds'):
        key = line.NAME.replace(' ', '_')
        data.add(
            models.SoundSegment,
            key,
            id=key,
            name=line.GRAPHEME,
            description=line.NAME,
            generated=True if line.GENERATED else False,
            unicode=line.UNICODE,
        )

    english = data.add(
        common.Language, 'eng',
        id='eng',
        name='English')

    for line in iterrows(clts, 'index'):
        c = data.add(
            models.Transcription,
            line.NAME,
            id=line.NAME,
            name=line.NAME,
            description=line.DESCRIPTION,
            datatype=getattr(models.Datatype, line.TYPE)
        )
        for id_ in line.REFS.split(', '):
            common.ContributionReference(source=data['Source'][id_], contribution=c)

    for line in iterrows(clts, 'graphemes'):
        key = line.DATASET + ':' + line.NAME+':'+line.GRAPHEME
        if key not in data['Grapheme']:
            sound_id = line.NAME.replace(' ', '_')
            vs = data['ValueSet'].get((line.DATASET, line.NAME))
            if not vs:
                try:
                    vs = data.add(
                        common.ValueSet,
                        (line.DATASET, line.NAME),
                        id=key,
                        description=line.NAME,
                        language=english,
                        contribution=data['Transcription'][line.DATASET],
                        parameter=data['SoundSegment'][sound_id]
                    )
                except:
                    print(line)
                    raise
            data.add(
                models.Grapheme,
                key,
                id=key,
                name=line.GRAPHEME,
                description=line.NAME,
                frequency=line.FREQUENCY or 0,
                image=line.IMAGE,
                url=line.URL,
                valueset=vs
            )


def prime_cache(args):  # pragma: no cover
    """If data needs to be denormalized for lookup, do that here.
    This procedure should be separate from the db initialization, because
    it will have to be run periodiucally whenever data has been updated.
    """
    for p in DBSession.query(common.Parameter) \
            .options(joinedload(common.Parameter.valuesets).joinedload(common.ValueSet.values)):
        p.representation = sum(len(vs.values) for vs in p.valuesets)

    for p in DBSession.query(common.Contribution)\
            .options(joinedload(common.Contribution.valuesets).joinedload(common.ValueSet.values)):
        p.items = sum(len(vs.values) for vs in p.valuesets)


if __name__ == '__main__':  # pragma: no cover
    initializedb(create=main, prime_cache=prime_cache)
    sys.exit(0)

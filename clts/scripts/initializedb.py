from __future__ import unicode_literals
import sys

from clld.scripts.util import initializedb, Data, bibtex2source
from clld.db.meta import DBSession
from clld.db.models import common

from clld.lib.bibtex import Database

import clts
from clts import models

from pyclts.util import data_path, pkg_path
from clldutils.dsv import reader
from clldutils.misc import slug

import os

def main(args):
    data = Data()

    for rec in Database.from_file(
            data_path('references.bib'), lowercase=False):
        source = data.add(common.Source, rec.id, _obj=bibtex2source(rec))
    
    dataset = common.Dataset(
        id=clts.__name__,
        name="CLTS",
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
    for i, name in enumerate(['Johann-Mattis List', 'Cormac Anderson', 'Tiago Tresoldi', 
        'Thiago Chacon', 'Robert Forkel']):
        c = common.Contributor(id=slug(name), name=name)
        dataset.editors.append(common.Editor(contributor=c, ord=i))

    for i, line in enumerate(reader(data_path('sounds.tsv'), delimiter='\t',
            namedtuples=True)):
        if not i % 100:
            print('-', end="")
        key = line.NAME.replace(' ', '_')
        data.add(
                models.SoundSegment,
                key,
                id=key,
                name = line.NAME,
                grapheme=line.GRAPHEME,
                aliases=line.ALIASES,
                representation=len(line.REFLEXES.split(',')),
                reflexes = line.REFLEXES,
                generated = True if line.GENERATED else False,
                unicode = line.UNICODE,
                )
    print('')
    english = data.add(
        common.Language, 'eng',
        id='eng',
        name='English')



    contributions = {}
    for line in reader(data_path('datasets.tsv'),
            delimiter='\t', namedtuples=True):
        contributions[line.NAME] = data.add(
                models.CLTSDataSet,
                line.NAME,
                id=line.NAME,
                name=line.NAME,
                description=line.DESCRIPTION,
                datatype=line.TYPE
                )
        for id_ in line.REFS.split(', '):
            common.ContributionReference(
                    source=data['Source'][id_],
                    contribution=contributions[line.NAME])
    
        
    visited = set()
    for i, line in enumerate(reader(data_path('graphemes.tsv'), delimiter="\t",
            namedtuples=True)):
        if not i % 100: print('-', end='')
        key = line.DATASET + ':' + line.NAME+':'+line.GRAPHEME
        if key not in visited:
            sound_id = line.NAME.replace(' ', '_')
            vs = common.ValueSet(
                    id=key,
                    description=line.NAME,
                    language=english,
                    contribution=contributions[line.DATASET],
                    parameter=data['SoundSegment'][sound_id]
                    )
            data.add(
                    models.Grapheme,
                    key,
                    id=key,
                    grapheme=line.GRAPHEME,
                    bipa_grapheme=line.BIPA,
                    name=line.NAME,
                    dataset=line.DATASET,
                    datatype=line.DATATYPE,
                    frequency=line.FREQUENCY or 0,
                    image=line.IMAGE,
                    url=line.URL,
                    valueset=vs
                    )
            visited.add(key)
    print('-')



def prime_cache(args):
    """If data needs to be denormalized for lookup, do that here.
    This procedure should be separate from the db initialization, because
    it will have to be run periodiucally whenever data has been updated.
    """


if __name__ == '__main__':
    initializedb(create=main, prime_cache=prime_cache)
    sys.exit(0)

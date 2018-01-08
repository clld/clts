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

import os

def main(args):
    data = Data()

    for rec in Database.from_file(
            pkg_path('references', 'references.bib'), lowercase=False):
        source = data.add(common.Source, rec.id, _obj=bibtex2source(rec))


    for i, line in enumerate(reader(data_path('sounds.tsv'), delimiter='\t',
            namedtuples=True)):
        if not i % 100:
            print('-', end="")
        key = line.ID.replace(' ', '_')
        data.add(
                models.SoundSegment,
                key,
                id=key,
                name = line.ID,
                grapheme=line.GRAPHEME,
                aliases=line.ALIASES,
                transcription_systems=line.TRANSCRIPTION_SYSTEMS,
                transcription_data=line.TRANSCRIPTION_DATA,
                sound_classes=line.SOUND_CLASSES,
                representation=int(line.REPRESENTATION or 0)
                )
    print('')
    english = data.add(
        common.Language, 'eng',
        id='eng',
        name='English')



    contributions = {}
    for line in reader(pkg_path('transcriptiondata', 'transcriptiondata.tsv'),
            delimiter='\t', namedtuples=True):
        contributions[line.ID] = data.add(
                models.TranscriptionData,
                line.ID,
                id=line.ID,
                name=line.ID,
                description=line.DESCRIPTION
                )
        for id_ in line.REFS.split(', '):
            common.ContributionReference(
                    source=data['Source'][id_],
                    contribution=contributions[line.ID])
    
        
    visited = set()
    for i, line in enumerate(reader(data_path('graphemes.tsv'), delimiter="\t",
            namedtuples=True)):
        if not i % 100: print('-', end='')
        key = line.TRANSCRIPTION_DATA + ':' + line.NAME+':'+line.GRAPHEME
        if key not in visited:
            sound_id = line.NAME.replace(' ', '_')
            vs = common.ValueSet(
                    id=key,
                    description=line.NAME,
                    language=english,
                    contribution=contributions[line.TRANSCRIPTION_DATA],
                    parameter=data['SoundSegment'][sound_id]
                    )
            data.add(
                    models.Grapheme,
                    key,
                    id=key,
                    grapheme=line.GRAPHEME,
                    name=line.NAME,
                    transcription_data=line.TRANSCRIPTION_DATA,
                    frequency=line.FREQUENCY or 0,
                    image=line.IMAGE,
                    url=line.URL,
                    valueset=vs
                    )
            visited.add(key)
    print('-')

    dataset = common.Dataset(id=clts.__name__, domain='clts.clld.org')
    DBSession.add(dataset)


def prime_cache(args):
    """If data needs to be denormalized for lookup, do that here.
    This procedure should be separate from the db initialization, because
    it will have to be run periodiucally whenever data has been updated.
    """


if __name__ == '__main__':
    initializedb(create=main, prime_cache=prime_cache)
    sys.exit(0)

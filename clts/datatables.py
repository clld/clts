from __future__ import unicode_literals

from sqlalchemy import and_
from sqlalchemy.orm import aliased, joinedload, joinedload_all

from clld.web.datatables.base import Col, LinkCol, IdCol, DetailsRowLinkCol, IntegerIdCol
from clld.web.datatables.contribution import Contributions, ContributorsCol
from clld.web.datatables.contributor import Contributors, NameCol, ContributionsCol
from clld.web.datatables.parameter import Parameters
from clld.web.datatables.value import Values
from clld.web.util.helpers import linked_references
from clld.web.util.htmllib import HTML
from clld.db.meta import DBSession
from clld.db.models.common import (
    Value, Value_data, ValueSet, Parameter, Contribution, ContributionContributor,
    ContributionReference,
)
from clld.db.util import get_distinct_values, icontains


class Authors(Contributors):
    def base_query(self, query):
        return query.join(ContributionContributor)

    def col_defs(self):
        return [
            NameCol(self, 'name'),
            ContributionsCol(self, ''),
        ]

class SoundSegments(Parameters):
    def col_defs(self):
        return [
            Col(self, 'grapheme', sTitle='Grapheme'),
            LinkCol(self, 'name'),
            Col(self, 'aliases', sTitle='Aliases'),
            Col(self, 'representation', sTitle='Representation')
        ]

class Graphemes(Values):
    def col_defs(self):
        return [
                Col(self, 'grapheme', sTitle='Grapheme'), 
                LinkCol(self, 'name', get_objects=lambda v:
                    v.valueset.parameter),
                Col(self, 'frequency', sTitle='Frequency'),
                LinkCol(self, 'transcription_data', get_object=lambda v:
                    v.valueset.contribution, sTitle="Dataset"),
                Col(self, 'url', sTitle="URL")
                ]

class RefsCol(Col):
    __kw__ = {'bSortable': False, 'bSearchable': False}

    def format(self, item):
        return linked_references(self.dt.req, item)

class Datasets(Contributions):
    def col_defs(self):
        return [
                LinkCol(self, 'name'),
                Col(self, 'description', sTitle='Description'),
                RefsCol(self, 'sources'),
                ]

def includeme(config):
    config.register_datatable('parameters', SoundSegments)
    config.register_datatable('values', Graphemes)
    config.register_datatable('contributions', Datasets)


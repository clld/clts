from zope.interface import implementer
from sqlalchemy import (
    Column,
    Unicode,
    Integer,
    Boolean,
    ForeignKey,
)

from clld import interfaces
from clld.db.meta import CustomModelMixin
from clld.db.models.common import Value, Parameter, Contribution
from clld.util import DeclEnum


class Datatype(DeclEnum):
    ts = 'transcription system', ''
    td = 'transcription data', ''
    sc = 'sound class system', ''


@implementer(interfaces.IParameter)
class SoundSegment(CustomModelMixin, Parameter):
    # name: grapheme
    # description: the feature-based name
    pk = Column(Integer, ForeignKey('parameter.pk'), primary_key=True)
    representation = Column(Integer)
    unicode = Column(Unicode)
    generated = Column(Boolean)


@implementer(interfaces.IValue)
class Grapheme(CustomModelMixin, Value):
    # name: grapheme
    # description: the feature-based name
    pk = Column(Integer, ForeignKey('value.pk'), primary_key=True)
    url = Column(Unicode)
    features = Column(Unicode)
    image = Column(Unicode)
    dataset = Column(Unicode)


@implementer(interfaces.IContribution)
class Transcription(CustomModelMixin, Contribution):
    pk = Column(Integer, ForeignKey('contribution.pk'), primary_key=True)
    items = Column(Integer)
    datatype = Column(Datatype.db_type())

from zope.interface import implementer
from sqlalchemy import (
    Column,
    String,
    Unicode,
    Integer,
    Boolean,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.hybrid import hybrid_property

from clld import interfaces
from clld.db.meta import Base, CustomModelMixin
from clld.db.models.common import Language, Value, Parameter, Contribution


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
    datatype = Column(Unicode)
    dataset = Column(Unicode)


@implementer(interfaces.IContribution)
class CLTSDataSet(CustomModelMixin, Contribution):
    pk = Column(Integer, ForeignKey('contribution.pk'), primary_key=True)
    items = Column(Integer)
    datatype = Column(Unicode)

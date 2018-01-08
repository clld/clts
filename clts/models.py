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


#-----------------------------------------------------------------------------
# specialized common mapper classes
#-----------------------------------------------------------------------------
#@implementer(interfaces.ILanguage)
#class cltsLanguage(CustomModelMixin, Language):
#    pk = Column(Integer, ForeignKey('language.pk'), primary_key=True)

@implementer(interfaces.IParameter)
class SoundSegment(CustomModelMixin, Parameter):
    pk = Column(Integer, ForeignKey('parameter.pk'), primary_key=True)
    grapheme = Column(Unicode)
    aliases = Column(Unicode)
    representation = Column(Integer)
    transcription_systems = Column(Unicode)
    transcription_data = Column(Unicode)
    sound_classes = Column(Unicode)

@implementer(interfaces.IValue)
class Grapheme(CustomModelMixin, Value):
    pk = Column(Integer, ForeignKey('value.pk'), primary_key=True)
    grapheme = Column(Unicode)
    transcription_data = Column(Unicode)
    url = Column(Unicode)
    features = Column(Unicode)
    image = Column(Unicode)

@implementer(interfaces.IContribution)
class TranscriptionData(CustomModelMixin, Contribution):
    pk = Column(Integer, ForeignKey('contribution.pk'), primary_key=True)
    items = Column(Integer)
    

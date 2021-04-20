from zope.interface import implementer
from sqlalchemy import (
    Column,
    Unicode,
    Integer,
    Boolean,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from clld import interfaces
from clld.db.meta import CustomModelMixin, Base
from clld.db.models.common import Value, Parameter, Contribution, IdNameDescriptionMixin
from clld.util import DeclEnum

from clts import interfaces as clts_interfaces


class Datatype(DeclEnum):
    ts = 'transcription system', ''
    td = 'transcription data', ''
    sc = 'sound class system', ''


@implementer(clts_interfaces.IFeature)
class Feature(Base, IdNameDescriptionMixin):
    sound_type = Column(Unicode)
    feature = Column(Unicode)
    value = Column(Unicode)
    count_sounds = Column(Integer)


class SoundSegmentFeature(Base):
    __table_args__ = (UniqueConstraint('soundsegment_pk', 'feature_pk'),)

    soundsegment_pk = Column(Integer, ForeignKey('soundsegment.pk'))
    feature_pk = Column(Integer, ForeignKey('feature.pk'))


@implementer(interfaces.IParameter)
class SoundSegment(CustomModelMixin, Parameter):
    # name: grapheme
    # description: the feature-based name
    pk = Column(Integer, ForeignKey('parameter.pk'), primary_key=True)
    type = Column(Unicode)
    representation = Column(Integer)
    unicode = Column(Unicode)
    generated = Column(Boolean)
    color = Column(Unicode)
    features = relationship(
        Feature, secondary=SoundSegmentFeature.__table__, backref='sounds')


@implementer(interfaces.IValue)
class Grapheme(CustomModelMixin, Value):
    # name: grapheme
    # description: the feature-based name
    pk = Column(Integer, ForeignKey('value.pk'), primary_key=True)
    url = Column(Unicode)
    features = Column(Unicode)
    image = Column(Unicode)
    audio = Column(Unicode)
    dataset = Column(Unicode)


@implementer(interfaces.IContribution)
class Transcription(CustomModelMixin, Contribution):
    pk = Column(Integer, ForeignKey('contribution.pk'), primary_key=True)
    items = Column(Integer)
    datatype = Column(Datatype.db_type())
    with_url = Column(Boolean)
    with_audio = Column(Boolean)
    with_image = Column(Boolean)

from sqlalchemy import Column, String, ForeignKey, text, UniqueConstraint
from sqlalchemy.dialects.mysql import INTEGER, DATETIME
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

# create base class for each table model class
Base = declarative_base()


class DataType(Base):
    # table name
    __tablename__ = 'data_types'
    __table_args__ = (
        {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4'}
    )
    # columns
    name = Column('name', String(16), primary_key=True)
    # relationship
    data = relationship("Datum", backref='data_types')


class Region(Base):
    # table name
    __tablename__ = 'regions'
    __table_args__ = (
        {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4'}
    )
    # columns
    name = Column('name', String(16), primary_key=True)
    # relationship
    buckets = relationship("Bucket", backref='regions')
    objects = relationship("Object", backref='regions')


class Bucket(Base):
    # table name
    __tablename__ = 'buckets'
    __table_args__ = (
        {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4'}
    )

    # columns
    id = Column('id', INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    user_id = Column('user_id', String(16), nullable=False)
    name = Column('name', String(32), nullable=False)
    region = Column('region', String(16), ForeignKey('regions.name'), nullable=False)
    created_at = Column(
        'created_at',
        DATETIME(fsp=6),
        nullable=False,
        server_default=text('CURRENT_TIMESTAMP(6)')
    )
    updated_at = Column(
        'updated_at',
        DATETIME(fsp=6),
        nullable=False,
        server_default=text('CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6)')
    )
    deleted_at = Column('deleted_at', DATETIME(fsp=6), nullable=False)
    object = relationship('Object', backref='bucket')  # One To Many
    UniqueConstraint('user_id', 'name', 'region', 'deleted_at', name='unq_bucket_user_id_name_region')

    @property
    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'region': self.region,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'deleted_at': self.deleted_at
        }


class Object(Base):
    # table name
    __tablename__ = 'objects'
    __table_args__ = (
        {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4'}
    )

    # columns
    id = Column('id', INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    user_id = Column('user_id', String(16), nullable=False)
    name = Column('name', String(32), nullable=False)
    region = Column('region', String(16), ForeignKey('regions.name'), nullable=False)
    version = Column('version', String(32), nullable=False)
    bucket_id = Column('bucket_id', INTEGER(unsigned=True), ForeignKey('buckets.id'), nullable=False)
    created_at = Column(
        'created_at',
        DATETIME(fsp=6),
        nullable=False,
        server_default=text('CURRENT_TIMESTAMP(6)')
    )
    updated_at = Column(
        'updated_at',
        DATETIME(fsp=6),
        nullable=False,
        server_default=text('CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6)')
    )
    deleted_at = Column('deleted_at', DATETIME(fsp=6), nullable=False)
    data = relationship('Datum', backref='objects')  # One To Many
    UniqueConstraint('name', 'version', 'deleted_at', name='unq_name_version')

    @property
    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'region': self.region,
            'version': self.version,
            'bucket_id': self.bucket_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'deleted_at': self.deleted_at
        }


class Datum(Base):
    # table name
    __tablename__ = 'data'
    __table_args__ = (
        {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4'}
    )

    # columns
    id = Column('id', INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    user_id = Column('user_id', String(16), nullable=False)
    name = Column('name', String(32), nullable=False)
    data_type = Column('data_type', String(16), ForeignKey('data_types.name'), nullable=False)
    object_id = Column('object_id', INTEGER(unsigned=True), ForeignKey('objects.id'), nullable=False)
    created_at = Column(
        'created_at',
        DATETIME(fsp=6),
        nullable=False,
        server_default=text('CURRENT_TIMESTAMP(6)')
    )
    updated_at = Column(
        'updated_at',
        DATETIME(fsp=6),
        nullable=False,
        server_default=text('CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6)')
    )
    deleted_at = Column('deleted_at', DATETIME(fsp=6), nullable=False)
    UniqueConstraint('user_id', 'name', 'deleted_at', name='unq_user_id_name')

    @property
    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'data_type': self.data_type,
            'object_id': self.object_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'deleted_at': self.deleted_at
        }

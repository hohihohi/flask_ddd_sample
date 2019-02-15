from sqlalchemy import Column, String, DateTime, ForeignKey, text, UniqueConstraint
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


class Region(Base):
    # table name
    __tablename__ = 'regions'
    __table_args__ = (
        {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4'}
    )
    # columns
    name = Column('name', String(16), primary_key=True)


class Datum(Base):
    # table name
    __tablename__ = 'data'
    __table_args__ = (
        UniqueConstraint('user_id', 'name', 'deleted_at', name='unq_user_id_name'),
        {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4'}
    )

    # columns
    id = Column('id', INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    user_id = Column('user_id', String(16), nullable=False)
    name = Column('name', String(32), nullable=False)
    data_type = Column('data_type', String(16), ForeignKey('data_types.name'), nullable=False)
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
    object = relationship('Objects', backref='data')
    # TODO: unique restriction (unq_user_id_name)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'data_type': self.data_type,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'deleted_at': self.deleted_at,
            'object': self.object
        }


class Bucket(Base):
    # table name
    __tablename__ = 'buckets'
    __table_args__ = (
        UniqueConstraint('user_id', 'name', 'region', 'deleted_at', name='unq_bucket_user_id_name_region'),
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
    object = relationship('Objects', backref='bucket')
    # TODO: unique restriction (unq_bucket_user_id_name_region )

    @property
    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'region': self.region,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'deleted_at': self.deleted_at,
            'object': self.object
        }


class Object(Base):
    # table name
    __tablename__ = 'objects'
    __table_args__ = (
        UniqueConstraint('data_id', 'name', 'deleted_at', name='unq_data_id_name'),
        UniqueConstraint('bucket_id', 'name', 'version', 'deleted_at', name='unq_bucket_id_name_version'),
        {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4'}
    )

    # columns
    id = Column('id', INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    user_id = Column('user_id', String(16), nullable=False)
    name = Column('name', String(32), nullable=False)
    region = Column('region', String(16), ForeignKey('regions.name'), nullable=False)
    version = Column('version', String(32), nullable=False)
    data_id = Column('data_id', INTEGER(unsigned=True), ForeignKey('data.id'), nullable=False)
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
    # TODO: unique restriction (object_region_fk, object_data_id_fk, object_bucket_id_fk)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'region': self.region,
            'version': self.version,
            'data_id': self.data_id,
            'bucket_id': self.bucket_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'deleted_at': self.deleted_at
        }

# -*- coding: utf-8 -*-
from datetime import datetime

from sqlalchemy import Column, types
from sqlservice import declarative_base

Model = declarative_base()


class Sample(Model):

    __tablename__ = 'sample'

    id = Column(types.Integer, primary_key=True)
    project_id = Column(types.String(32), nullable=False)
    lims_id = Column(types.String(32), unique=True)
    name = Column(types.String(128))
    created_at = Column(types.DateTime, default=datetime.now)

    reference_genome = Column(types.String(32))
    total_reads = Column(types.Integer)
    insert_size = Column(types.Integer)
    duplication_rate = Column(types.Float)
    mapped_rate = Column(types.Float)
    coverage_10x = Column(types.Float)
    coverage_30x = Column(types.Float)
    coverage_50x = Column(types.Float)
    coverage_100x = Column(types.Float)

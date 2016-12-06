# -*- coding: utf-8 -*-
from datetime import datetime

from sqlalchemy import Column, types
from sqlservice import declarative_base

Model = declarative_base()


class Sample(Model):

    __tablename__ = 'sample'

    id = Column(types.Integer, primary_key=True)
    lims_id = Column(types.String(32), unique=True)
    created_at = Column(types.DateTime, default=datetime.now)

    reference_genome = Column(types.String(32))
    insert_size = Column(types.Integer)
    duplication_rate = Column(types.Float)
    mapped_rate = Column(types.Float)
    coverage_10x = Column(types.Float)

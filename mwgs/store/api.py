# -*- coding: utf-8 -*-
from sqlservice import SQLClient

from .models import Model


def connect(db_uri):
    """Connect to database."""
    db = SQLClient({'SQL_DATABASE_URI': db_uri}, model_class=Model)
    return db


def connect_app(app):
    """Connect Flask application."""
    db = connect(app.config['SQL_DATABASE_URI'])
    return db


def build_sample(data):
    """Prepare data to match database interface."""
    parsed = {
        'lims_id': data['Sample Name'],
        'reference_genome': data['Reference Genome'],
        'inser_size': data['Median Insert Size'],
        'duplication_rate': data['Duplication Rate'],
        'mapped_rate': data['Fraction aligned to Reference'],
        'coverage10x_rate': data['Fraction of bases with cov >= 10X'],
    }
    return parsed


def duplication_rate(db):
    """Calculate times it takes to analyze a sample."""
    points = [{
        'name': sample.lims_id,
        'y': sample.duplication_rate,
    } for sample in db.Sample.find()]
    return points

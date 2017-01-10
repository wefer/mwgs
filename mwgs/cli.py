# -*- coding: utf-8 -*-
import os

import click
import yaml

from mwgs.store import api
from mwgs.core import Sample


@click.group()
def root():
    """Interact with the MWGS pipeline."""
    pass


@root.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('-p', '--parallel', is_flag=True)
@click.argument('sample_path')
def start(sample_path, parallel):
    """Start an analysis run."""
    analysis_sample = Sample(sample_path, parallel=parallel)
    analysis_sample.run_qc()
    analysis_sample.dump_metrics()


@root.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('-d', '--database', help='SQL connection string')
@click.argument('statistics', type=click.File('r'))
def add(database, statistics):
    """Load results into database."""
    db_uri = database or os.environ['MWGS_SQL_DATABASE_URI']
    db = api.connect(db_uri)
    if len(db.engine.table_names()) == 0:
        db.create_all()
    data = yaml.load(statistics)
    sample_data = api.build_sample(data)
    new_sample = db.Sample.save(sample_data)
    click.echo("added sample: {}".format(new_sample.lims_id))

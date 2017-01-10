# -*- coding: utf-8 -*-
import os

import click
import yaml

from mwgs.store import api
from mwgs.core import Sample


@click.group()
@click.option('-d', '--database', help='SQL connection string')
@click.pass_context
def root(context, database):
    """Interact with the MWGS pipeline."""
    context.obj = {
        'database': database or os.environ.get('MWGS_SQL_DATABASE_URI')
    }


@root.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('-p', '--parallel', is_flag=True)
@click.argument('sample_path')
@click.pass_context
def start(context, sample_path, parallel):
    """Start an analysis run."""
    analysis_sample = Sample(sample_path, parallel=parallel)
    analysis_sample.run_qc()
    analysis_sample.dump_metrics()
    # upload results to database
    out_path = os.path.join(sample_path, 'statistics.yml')
    context.invoke(add, statistics=out_path)


@root.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.argument('statistics', type=click.File('r'))
@click.pass_context
def add(context, database, statistics):
    """Load results into database."""
    db = api.connect(context.obj['database'])
    if len(db.engine.table_names()) == 0:
        db.create_all()
    data = yaml.load(statistics)
    sample_data = api.build_sample(data)
    new_sample = db.Sample.save(sample_data)
    click.echo("added sample: {}".format(new_sample.lims_id))

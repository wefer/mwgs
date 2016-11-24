# -*- coding: utf-8 -*-
import os

import click
import yaml

from mwgs.store import api


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('-d', '--database', help='SQL connection string')
@click.argument('statistics', type=click.File('r'))
def mwgs(database, statistics):
    """Load results into database."""
    db_uri = database or os.environ['MWGS_SQL_DATABASE_URI']
    db = api.connect(db_uri)
    if len(db.engine.table_names()) == 0:
        db.create_all()
    data = yaml.load(statistics)
    sample_data = api.build_sample(data)
    new_sample = db.Sample.save(sample_data)
    click.echo("added sample: {}".format(new_sample.lims_id))


if __name__ == '__main__':
    mwgs()

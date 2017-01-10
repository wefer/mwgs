# -*- coding: utf-8 -*-
"""#!/bin/bash -l
#SBATCH -A prod001
#SBATCH -n 16
#SBATCH -t 40:00:00
#SBATCH -J mwgs-{project}
#SBATCH -e /mnt/hds/proj/bioinfo/MICROBIAL/logs/mwgs-{project}.stderr.txt
#SBATCH -o /mnt/hds/proj/bioinfo/MICROBIAL/logs/mwgs-{project}.stdout.txt
#SBATCH --mail-type=FAIL
#SBATCH --mail-user={email}

shopt -s expand_aliases
source ~/.bashrc
source activate micro

for sample_path in $(find {project_path} -maxdepth 1 -mindepth 1 -type d)
do
    echo "processing: ${{sample_path}}"
    mwgs start --parallel "${{sample_path}}" &
done

wait
"""
import os
import subprocess

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


@root.command()
@click.option('-e', '--email', help='email to send errors to')
@click.argument('project_path')
@click.pass_context
def project(context, email, project_path):
    """Process all samples in a project."""
    project = os.path.basename(project_path)
    email = email or environ_email()
    script = __doc__.format(project=project, email=email,
                            project_path=project_path)
    script_path = os.path.join(project_path, 'run.sh')
    with open(script_path, 'w') as out_handle:
        out_handle.write(script)
    process = subprocess.Popen(['sbatch', script_path])
    process.wait()
    if process.returncode != 0:
        click.echo("ERROR: starting analysis, check the output")
        context.abort()


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
    with open(out_path, 'r') as out_handle:
        context.invoke(add, statistics=out_handle)


@root.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.argument('statistics', type=click.File('r'))
@click.pass_context
def add(context, statistics):
    """Load results into database."""
    db = api.connect(context.obj['database'])
    if len(db.engine.table_names()) == 0:
        db.create_all()
    data = yaml.load(statistics)
    sample_data = api.build_sample(data)
    existing_sample = db.Sample.filter_by(lims_id=sample_data['lims_id'])
    if existing_sample.first():
        click.echo("destroying existing samples")
        existing_sample.destroy()
    new_sample = db.Sample.save(sample_data)
    click.echo("added sample: {}".format(new_sample.lims_id))


def environ_email():
    """Guess email from sudo user environment variable."""
    username = os.environ.get('SUDO_USER')
    if username:
        return "{}@scilifelab.se".format(username)

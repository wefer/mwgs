# -*- coding: utf-8 -*-
import os

from flask import Flask, render_template
from flask_bootstrap import Bootstrap

from mwgs.store.models import Sample, Model
from mwgs.store import api
from .flask_sqlservice import FlaskSQLService

app = Flask(__name__)
BOOTSTRAP_SERVE_LOCAL = 'FLASK_DEBUG' in os.environ
TEMPLATES_AUTO_RELOAD = True
SQL_DATABASE_URI = os.environ['MWGS_SQL_DATABASE_URI']
app.config.from_object(__name__)


@app.route('/')
def index():
    projects = db.query(Sample.project_id).distinct()
    return render_template('mwgs/index.html', projects=projects)


@app.route('/projects/<project_id>')
def project(project_id):
    samples = db.Sample.filter_by(project_id=project_id)
    duplications = api.plot_data(samples, "duplication_rate")
    mapped = api.plot_data(samples, "mapped_rate")
    coverage = api.plot_data(samples, "coverage_10x")
    reads_coverage = api.plot_reads_coverage(samples)
    return render_template(
        'mwgs/project.html',
        samples=samples,
        project_id=project_id,
        duplications=duplications,
        mapped=mapped,
        coverage=coverage,
        reads_coverage=reads_coverage,
    )


@app.template_filter()
def percent(value):
    """Format number as percent."""
    return round(value * 100, 2)


# hookup extensions to app
Bootstrap(app)
db = FlaskSQLService(app=app, model_class=Model)

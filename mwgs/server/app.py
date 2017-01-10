# -*- coding: utf-8 -*-
import os

from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from mwgs.store.models import Sample
from mwgs.store import api

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
    samples = db.Sample.find(project_id=project_id)
    duplications = api.plot_data(samples, "duplication_rate")
    mapped = api.plot_data(samples, "mapped_rate")
    coverage = api.plot_data(samples, "coverage_10x")
    return render_template(
        'mwgs/project.html',
        samples=samples,
        project_id=project_id,
        duplications=duplications,
        mapped=mapped,
        coverage=coverage
    )


# hookup extensions to app
Bootstrap(app)
db = api.connect_app(app)

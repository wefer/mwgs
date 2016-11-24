# -*- coding: utf-8 -*-
import os

from flask import Flask, render_template
from flask_bootstrap import Bootstrap

from mwgs.store import api

app = Flask(__name__)
BOOTSTRAP_SERVE_LOCAL = 'FLASK_DEBUG' in os.environ
TEMPLATES_AUTO_RELOAD = True
SQL_DATABASE_URI = os.environ['MWGS_SQL_DATABASE_URI']
app.config.from_object(__name__)


@app.route('/')
def index():
    duplications = api.duplication_rate(db)
    return render_template('index.html', duplications=duplications)


# hookup extensions to app
Bootstrap(app)
db = api.connect_app(app)

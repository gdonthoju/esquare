# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present eSquare
"""

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from importlib import import_module
from datetime import datetime
import pytz

db = SQLAlchemy()
login_manager = LoginManager()


def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)


def register_blueprints(app):
    for module_name in ('authentication', 'home'):
        module = import_module('apps.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)


def configure_database(app):

    @app.before_first_request
    def initialize_database():
        db.create_all()

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()

def custom_format_date(app):
    @app.template_filter()
    # def format_datetime(unix_time, time_zone='Asia/Kolkata'): # needed if we want to specify timezone from env variable explicitly
    def format_datetime(unix_time):
        unix_time = str(int(int(unix_time)/1000))
        if unix_time == '':
            return ''
        unaware_dt = datetime.utcfromtimestamp(int(unix_time)).strftime("%m/%d/%Y %I:%M:%S %p")
        aware_dt = datetime.strptime(unaware_dt, "%m/%d/%Y %I:%M:%S %p")
        aware_dt = pytz.utc.localize(aware_dt)
        # est = pytz.timezone(time_zone)
        # aware_dt = est.normalize(aware_dt)
        return aware_dt

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    register_extensions(app)
    register_blueprints(app)
    configure_database(app)
    custom_format_date(app)
    return app

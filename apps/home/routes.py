# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.home import blueprint
from flask import render_template, request
from flask_login import login_required
from jinja2 import TemplateNotFound
from apps.authentication.models import eSquareObservations, eSquareDataProducers, eSquareDataConsumers

@blueprint.route('/index')
@login_required
def index():

    return render_template('home/index.html', segment='index')


@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        if template.startswith('notifications'):
            observations = eSquareObservations.query.all()
            return render_template("home/" + template, observations=observations, segment=segment)

        elif template.startswith('data_producers'):
            data_producers = eSquareDataProducers.query.all()
            return render_template("home/" + template, data_producers=data_producers, segment=segment)

        elif template.startswith('data_consumers'):
            data_consumers = eSquareDataConsumers.query.all()
            return render_template("home/" + template, data_consumers=data_consumers, segment=segment)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None

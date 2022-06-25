# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from typing import ItemsView
from apps.home import blueprint
from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required
from jinja2 import TemplateNotFound
from apps.authentication.models import eSquareObservations, eSquareDataProducers, eSquareDataConsumers
from apps.authentication.forms import UploadDataProducersExcelForm
import pandas
from werkzeug.utils import secure_filename
import os
import datetime
from apps import db
from flask_login import (
    current_user
)

UPLOAD_FOLDER = '/home/seera/Documents/per/esquare/apps/home/temp_uploads/'
ALLOWED_EXTENSIONS = {'xls', 'xlsx'}

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


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# @blueprint.route('/data_producers_test', methods=['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
#         # check if the post request has the file part
#         if 'file' not in request.files:
#             flash('No file part')
#             return redirect(request.url)
#         file = request.files['file']
#         # If the user does not select a file, the browser submits an
#         # empty file without a filename.
#         if file.filename == '':
#             flash('No selected file')
#             return redirect(request.url)
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             file.save(os.path.join(UPLOAD_FOLDER, filename))
#             excelData = pandas.read_excel("/home/seera/Documents/per/esquare/apps/home/temp_uploads/"+filename,engine='openpyxl',dtype=object,header=None)
#             # print("excelData",excelData.values.tolist())

#             for itemww in excelData.values.tolist():
#                 print(itemww)

#             return redirect(url_for('download_file', name=filename))

#     return '''
#     <!doctype html>
#     <title>Upload new File</title>
#     <h1>Upload new File</h1>
#     <form method=post enctype=multipart/form-data>
#       <input type=file name=file>
#       <input type=submit value=Upload>
#     </form>
#     '''


@blueprint.route('/data_producers', methods=['GET', 'POST'])
@login_required
def route_data_producers():
    # Detect the current page
    segment = get_segment(request)
    upload_data_producers_excel_form = UploadDataProducersExcelForm(request.form)
    data_producers = eSquareDataProducers.query.all()
    if request.method == 'POST' and 'excel_upload_button' in request.form.keys():
        
        if 'excelFilePath' not in request.files:
            flash('No file part')
            print('No file part')
        file = request.files['excelFilePath']
        print('file data' , file)
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            print('No selected file')
            flash('No selected file')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            print("FILENAME" , UPLOAD_FOLDER + filename);
            excelData = pandas.read_excel(UPLOAD_FOLDER + filename,engine='openpyxl',dtype=object)
            # print("excelData",excelData.to_dict())
            excelDataAsList = excelData.values.tolist()

            for dataItem in excelDataAsList:
                dataProducerExcelRowAdd = {}
                dataProducerExcelRowAdd['producerApplicationName'] = dataItem[0]
                dataProducerExcelRowAdd['description'] = dataItem[1]
                dataProducerExcelRowAdd['lineOfBusiness'] = dataItem[2]
                dataProducerExcelRowAdd['dataDomain'] = dataItem[3]
                dataProducerExcelRowAdd['businessOwnerName'] = dataItem[4]
                dataProducerExcelRowAdd['businessOwnerEmail'] = dataItem[5]
                dataProducerExcelRowAdd['technicalOwnerName'] = dataItem[6]
                dataProducerExcelRowAdd['technicalOwnerEmail'] = dataItem[7]
                dataProducerExcelRowAdd['msg_batch_apis_name'] = dataItem[8]
                dataProducerExcelRowAdd['msg_batch_apis_description'] = dataItem[9]
                dataProducerExcelRowAdd['msg_batch_apis_type'] = dataItem[10]
                dataProducerExcelRowAdd['dataProducerOn'] = int(datetime.datetime.now().timestamp() * 1000)
                dataProducerExcelRowAdd['dataProducerBy'] = current_user.get_id()
                dataProducerAdd = eSquareDataProducers(**dataProducerExcelRowAdd)
                # print(dataProducerAdd)
                db.session.add(dataProducerAdd)
                db.session.commit()
                print(dataItem)
        return render_template("home/data_producers.html", data_producers=data_producers, segment=segment, form=upload_data_producers_excel_form)
    else:
        return render_template("home/data_producers.html", data_producers=data_producers, segment=segment, form=upload_data_producers_excel_form)
# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present eSquare
"""

from typing import ItemsView
from apps.home import blueprint
from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required
from jinja2 import TemplateNotFound
from apps.authentication.models import eSquareDataSets, eSquareObservations, eSquareDataProducers, eSquareDataConsumers, eSquareDataSources, eSquareBusinessGlossary, eSquareDataCatalogue, eSquareDataSetFields
from apps.authentication.forms import UniversalSearchForm, UploadDataProducersExcelForm, UploadDataSourcesExcelForm, UploadDataConsumersExcelForm, UploadBusinessGlossarysExcelForm, UploadDataCataloguesExcelForm, CreateDataSetForm, EditDataSetForm, SearchQueryForm
import pandas
import numpy
from werkzeug.utils import secure_filename
import os
import datetime
from sqlalchemy import or_
from apps import db
from flask_login import (
    current_user
)

UPLOAD_FOLDER = '/Users/girishdonthoju/Documents/development/esquare/apps/home/temp_uploads/'
ALLOWED_EXTENSIONS = {'xls', 'xlsx'}

@blueprint.route('/index')
@login_required
def index():

    universal_search_form = UniversalSearchForm(request.form)
    counts_data = {}
    counts_data['data_sources_count'] = eSquareDataSources.query.count()
    counts_data['business_glossary_count'] = eSquareBusinessGlossary.query.count()
    counts_data['data_catalogue_count'] = eSquareDataCatalogue.query.count()
    counts_data['hits_count'] = '#'
    counts_data['data_producers_count'] = eSquareDataProducers.query.count()
    counts_data['data_consumers_count'] = eSquareDataConsumers.query.count()
    counts_data['data_sets_count'] = eSquareDataSets.query.count()
    counts_data['data_observability_count'] = eSquareObservations.query.count()

    return render_template('home/index.html', segment='index', counts_data = counts_data, form = universal_search_form)


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

@blueprint.route('/data_sources', methods=['GET', 'POST'])
@login_required
def route_data_sources():
    # Detect the current page
    segment = get_segment(request)
    upload_data_sources_excel_form = UploadDataSourcesExcelForm(request.form)
    data_sources = eSquareDataSources.query.all()
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
            print("FILENAME" , UPLOAD_FOLDER + filename)
            excelData = pandas.read_excel(UPLOAD_FOLDER + filename,engine='openpyxl',dtype=object)
            # print("excelData",excelData.to_dict())
            excelDataAsList = excelData.values.tolist()

            for dataItem in excelDataAsList:
                dataSourceExcelRowAdd = {}

                dataSourceExcelRowAdd['applicationName'] = dataItem[0]
                dataSourceExcelRowAdd['description'] = dataItem[1]
                dataSourceExcelRowAdd['lineOfBusiness'] = dataItem[2]
                dataSourceExcelRowAdd['businessDomain'] = dataItem[3]
                dataSourceExcelRowAdd['dataDomain'] = dataItem[4]
                dataSourceExcelRowAdd['businessOwnerName'] = dataItem[5]
                dataSourceExcelRowAdd['businessOwnerEmail'] = dataItem[6]
                dataSourceExcelRowAdd['technicalOwnerName'] = dataItem[7]
                dataSourceExcelRowAdd['technicalOwnerEmail'] = dataItem[8]
                dataSourceExcelRowAdd['additionalInformation'] = dataItem[9]
                dataSourceExcelRowAdd['dataSourceOn'] = int(datetime.datetime.now().timestamp() * 1000)
                dataSourceExcelRowAdd['dataSourceBy'] = current_user.get_id()
                dataSourceAdd = eSquareDataSources(**dataSourceExcelRowAdd)
                # print(dataProducerAdd)
                db.session.add(dataSourceAdd)
                db.session.commit()
                print(dataItem)
                # os.remove(UPLOAD_FOLDER + filename)
        return redirect("data_sources")
        # return render_template("home/data_sources.html", data_sources=data_sources, segment=segment, form=upload_data_sources_excel_form)
    else:
        return render_template("home/data_sources.html", data_sources=data_sources, segment=segment, form=upload_data_sources_excel_form)

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
            print("FILENAME" , UPLOAD_FOLDER + filename)
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
                # os.remove(UPLOAD_FOLDER + filename)
        return redirect("data_producers")
        # return render_template("home/data_producers.html", data_producers=data_producers, segment=segment, form=upload_data_producers_excel_form)
    else:
        return render_template("home/data_producers.html", data_producers=data_producers, segment=segment, form=upload_data_producers_excel_form)

@blueprint.route('/data_consumers', methods=['GET', 'POST'])
@login_required
def route_data_consumers():
    # Detect the current page
    segment = get_segment(request)
    upload_data_consumers_excel_form = UploadDataConsumersExcelForm(request.form)
    data_consumers = eSquareDataConsumers.query.all()
    if request.method == 'POST' and 'excel_upload_button' in request.form.keys():

        if 'excelFilePath' not in request.files:
            flash('No file part')
            print('No file part')
        file = request.files['excelFilePath']
        print('file data', file)
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            print('No selected file')
            flash('No selected file')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            print("FILENAME", UPLOAD_FOLDER + filename)
            excelData = pandas.read_excel(UPLOAD_FOLDER + filename, engine='openpyxl', dtype=object)
            # print("excelData",excelData.to_dict())
            excelDataAsList = excelData.values.tolist()

            for dataItem in excelDataAsList:
                dataConsumerExcelRowAdd = {}
                dataConsumerExcelRowAdd['consumerApplicationName'] = dataItem[0]
                dataConsumerExcelRowAdd['description'] = dataItem[1]
                dataConsumerExcelRowAdd['lineOfBusiness'] = dataItem[2]
                dataConsumerExcelRowAdd['dataDomain'] = dataItem[3]
                dataConsumerExcelRowAdd['businessOwnerName'] = dataItem[4]
                dataConsumerExcelRowAdd['businessOwnerEmail'] = dataItem[5]
                dataConsumerExcelRowAdd['technicalOwnerName'] = dataItem[6]
                dataConsumerExcelRowAdd['technicalOwnerEmail'] = dataItem[7]
                dataConsumerExcelRowAdd['msg_batch_apis_name'] = dataItem[8]
                dataConsumerExcelRowAdd['msg_batch_apis_description'] = dataItem[9]
                dataConsumerExcelRowAdd['msg_batch_apis_type'] = dataItem[10]
                dataConsumerExcelRowAdd['dataConsumerOn'] = int(datetime.datetime.now().timestamp() * 1000)
                dataConsumerExcelRowAdd['dataConsumerBy'] = current_user.get_id()
                dataConsumerAdd = eSquareDataConsumers(**dataConsumerExcelRowAdd)
                print(dataConsumerExcelRowAdd)
                db.session.add(dataConsumerAdd)
                db.session.commit()
                print(dataItem)
        return redirect("data_consumers")
        # return render_template("home/data_producers.html", data_producers=data_producers, segment=segment, form=upload_data_producers_excel_form)
    else:
        return render_template("home/data_consumers.html", data_consumers=data_consumers, segment=segment,
                               form=upload_data_consumers_excel_form)

@blueprint.route('/business_glossary', methods=['GET', 'POST'])
@login_required
def route_business_glossary():
    # Detect the current page
    segment = get_segment(request)
    upload_business_glossary_excel_form = UploadBusinessGlossarysExcelForm(request.form)
    business_glossary = eSquareBusinessGlossary.query.all()
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
            print("FILENAME" , UPLOAD_FOLDER + filename)
            excelData = pandas.read_excel(UPLOAD_FOLDER + filename,engine='openpyxl',dtype=object)
            # print("excelData",excelData.to_dict())
            excelDataAsList = excelData.values.tolist()

            for dataItem in excelDataAsList:
                businessGlossaryExcelRowAdd = {}

                businessGlossaryExcelRowAdd['businessGlossaryTerm'] = dataItem[0]
                businessGlossaryExcelRowAdd['businessDefinition'] = dataItem[1]
                businessGlossaryExcelRowAdd['businessDomain'] = dataItem[2]
                businessGlossaryExcelRowAdd['termSource'] = dataItem[3]
                businessGlossaryExcelRowAdd['dataDomain'] = dataItem[4]
                businessGlossaryExcelRowAdd['businessSteward'] = dataItem[5]
                businessGlossaryExcelRowAdd['businessGlossaryOn'] = int(datetime.datetime.now().timestamp() * 1000)
                businessGlossaryExcelRowAdd['businessGlossaryBy'] = current_user.get_id()
                businessGlossaryAdd = eSquareBusinessGlossary(**businessGlossaryExcelRowAdd)
                # print(dataProducerAdd)
                db.session.add(businessGlossaryAdd)
                db.session.commit()
                print(dataItem)
                # os.remove(UPLOAD_FOLDER + filename)
        return redirect("business_glossary")
        # return render_template("home/business_glossary.html", business_glossary=business_glossary, segment=segment, form=upload_business_glossary_excel_form)
    else:
        return render_template("home/business_glossary.html", business_glossary=business_glossary, segment=segment, form=upload_business_glossary_excel_form)

@blueprint.route('/data_catalogue', methods=['GET', 'POST'])
@login_required
def route_data_catalogue():
    # Detect the current page
    segment = get_segment(request)
    upload_data_catalogue_excel_form = UploadDataCataloguesExcelForm(request.form)
    
    search_query_form = SearchQueryForm(request.form)
    search_query = ''

    if request.method == 'GET' and 'search_query' in request.args.keys():
        search_query = request.args.get('search_query')
        print("Args : " , search_query)
        data_catalogue = eSquareDataCatalogue.query.filter(or_(eSquareDataCatalogue.attributeName.contains(search_query),eSquareDataCatalogue.attributeDescription.contains(search_query)))
    else:
        data_catalogue = eSquareDataCatalogue.query.all()

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
            print("FILENAME" , UPLOAD_FOLDER + filename)
            excelData = pandas.read_excel(UPLOAD_FOLDER + filename,engine='openpyxl',dtype=object)
            # print("excelData",excelData.to_dict())
            excelDataAsList = excelData.values.tolist()

            for dataItem in excelDataAsList:
                dataCatalogueExcelRowAdd = {}

                dataCatalogueExcelRowAdd['attributeName'] = dataItem[0]
                dataCatalogueExcelRowAdd['attributeDescription'] = dataItem[1]
                dataCatalogueExcelRowAdd['tableName'] = dataItem[2]
                dataCatalogueExcelRowAdd['columnName'] = dataItem[3]
                dataCatalogueExcelRowAdd['columnDescription'] = dataItem[4]
                dataCatalogueExcelRowAdd['columnDatatype'] = dataItem[5]
                if dataItem[6] == 'Y':
                    dataCatalogueExcelRowAdd['isNullable'] = 1
                else:
                    dataCatalogueExcelRowAdd['isNullable'] = 0

                if dataItem[7] == 'Y':
                    dataCatalogueExcelRowAdd['isPrimaryKey'] = 1
                else:
                    dataCatalogueExcelRowAdd['isPrimaryKey'] = 0

                if dataItem[8] == 'Y':
                    dataCatalogueExcelRowAdd['isForeignKey'] = 1
                else:
                    dataCatalogueExcelRowAdd['isForeignKey'] = 0

                dataCatalogueExcelRowAdd['attributeSensitivity'] = dataItem[9]
                dataCatalogueExcelRowAdd['termSource'] = dataItem[10]
                dataCatalogueExcelRowAdd['possibleValues'] = dataItem[11]
                dataCatalogueExcelRowAdd['valuesDescription'] = dataItem[12]
                dataCatalogueExcelRowAdd['notes'] = dataItem[13]
                dataCatalogueExcelRowAdd['catalogueAttributeCreatedOn'] = int(datetime.datetime.now().timestamp() * 1000)
                dataCatalogueExcelRowAdd['catalogueAttributeCreatedBy'] = current_user.get_id()
                dataCatalogueExcelRowAdd['catalogueAttributeUpdatedBy'] = current_user.get_id()
                dataCatalogueAdd = eSquareDataCatalogue(**dataCatalogueExcelRowAdd)
                # print(dataProducerAdd)
                db.session.add(dataCatalogueAdd)
                db.session.commit()
                print(dataItem)
                # os.remove(UPLOAD_FOLDER + filename)
        return redirect("data_catalogue")
        # return render_template("home/data_catalogue.html", data_catalogue=data_catalogue, segment=segment, form=upload_data_catalogue_excel_form)
    else:
        return render_template("home/data_catalogue.html", data_catalogue=data_catalogue, segment=segment, form=upload_data_catalogue_excel_form, search_form=search_query_form,search_query=search_query)


@blueprint.route('/data_sets', methods=['GET', 'POST'])
@login_required
def route_data_sets():
    # Detect the current page
    segment = get_segment(request)
    upload_data_set_form = CreateDataSetForm(request.form)  
    search_query_form = SearchQueryForm(request.form)
    search_query = ''

    if request.method == 'GET' and 'search_query' in request.args.keys():
        search_query = request.args.get('search_query')
        print("Args : " , search_query)
        data_sets = eSquareDataSets.query.filter(or_(eSquareDataSets.dataSetName.contains(search_query),eSquareDataSets.dataSetDescription.contains(search_query)))
    else:
        data_sets = eSquareDataSets.query.all()
    
    # print("data_sets : ", data_sets)  

    if request.method == 'POST' and 'upload_dataset_button' in request.form.keys():
        dataSetName = request.form['dataSetName']
        dataSetDescription = request.form['dataSetDescription']
        # print("dataSetName : " , dataSetName)
        # print("dataSetDescription : " , dataSetDescription)
        dataSetValues = {}
        dataSetValues['dataSetName'] = dataSetName
        dataSetValues['dataSetDescription'] = dataSetDescription
        dataSetValues['dataSetCreatedOn'] = int(datetime.datetime.now().timestamp() * 1000)
        dataSetValues['dataSetCreatedBy'] = current_user.get_id()
        dataSetValues['dataSetUpdatedBy'] = current_user.get_id()

        dataSetAdd = eSquareDataSets(**dataSetValues)
        db.session.add(dataSetAdd)
        db.session.commit()
        dataSetID = dataSetAdd.id
        # print("dataSetID : " , dataSetID)

        if 'excelFilePath' not in request.files:
            flash('No file part')
            print('No file part')
        file = request.files['excelFilePath']
        # print('file data' , file)
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            # print('No selected file')
            flash('No selected file')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            # print("FILENAME" , UPLOAD_FOLDER + filename)
            excelData = pandas.read_excel(UPLOAD_FOLDER + filename,engine='openpyxl',header=0,dtype=object)
            # print("excelDataHead",excelData.head().to_dict())
            
            excelDataHead = excelData.head().keys().to_list()
            # print("excelDataHead",excelDataHead)
            excelDataAsList = excelData.values.tolist()
            # print("excelData",excelDataAsList)

            for dataItem in excelDataAsList:
                for iter in range(len(excelDataHead)):
                    # print("iter : ",iter)
                    # print(excelDataHead[iter],dataItem[iter])
                    dataSetExcelRowAdd = {}
                    dataSetExcelRowAdd['dataSetId'] = dataSetID
                    dataSetExcelRowAdd['dataSetFieldName'] = excelDataHead[iter]
                    dataSetExcelRowAdd['dataSetFieldValue'] = str(dataItem[iter])
                    dataSetExcelRowAdd['dataSetCreatedOn'] = int(datetime.datetime.now().timestamp() * 1000)
                    dataSetExcelRowAdd['dataSetCreatedBy'] = current_user.get_id()
                    dataSetExcelRowAdd['dataSetUpdatedBy'] = current_user.get_id()

                    dataSetFieldsAdd = eSquareDataSetFields(**dataSetExcelRowAdd)
                    db.session.add(dataSetFieldsAdd)
                    db.session.commit()
        return redirect("data_sets")
    else:
        return render_template("home/data_sets.html", data_sets=data_sets, segment=segment, form=upload_data_set_form, search_form=search_query_form,search_query=search_query)


@blueprint.route('/data_set/<data_set_id>', methods=['GET', 'POST'])
@login_required
def route_data_set(data_set_id):
    # Detect the current page
    segment = get_segment(request)
    edit_data_set_form = EditDataSetForm(request.form)
    data_set_field_names = eSquareDataSetFields.query.with_entities(eSquareDataSetFields.dataSetFieldName).filter_by(dataSetId=data_set_id).distinct()
    data_set_details = eSquareDataSets.query.filter_by(id=data_set_id)

    data_set_field_details_from_db = eSquareDataSetFields.query.filter_by(dataSetId=data_set_id)
    data_set_field_details = {}
    data_set_display_field_details = []
    for item in data_set_field_details_from_db:
        if item.dataSetFieldName in data_set_field_details:
            data_set_field_details[item.dataSetFieldName].append(item.dataSetFieldValue)
        else:
            data_set_field_details[item.dataSetFieldName] = []
            data_set_field_details[item.dataSetFieldName].append(item.dataSetFieldValue)

    # print("data_set_field_details_before_transpose : " , data_set_field_details)

    for listIter in data_set_field_details:
        data_set_display_field_details.append(data_set_field_details[listIter])

    # print("data_set_display_field_details : " , data_set_display_field_details)
    data_set_display_field_details = numpy.array(data_set_display_field_details).transpose().tolist()
    

    # print("data_set_id" , data_set_id)
    # print("data_sets : ", data_set_details)
    # print("data_set_display_field_detailsxxxx : ", data_set_display_field_details)
    # print("data_set_field_names : ", data_set_field_names)

    if request.method == 'POST' and 'delete_data_set' in request.form.keys():
        idDataSet = data_set_id
        print("delIdDataSet", idDataSet)
        eSquareDataSetFields.query.filter_by(dataSetId=idDataSet).delete()
        db.session.commit()
        eSquareDataSets.query.filter_by(id=idDataSet).delete()
        db.session.commit()
        return redirect("data_sets")
        # return render_template("home/data_set.html", data_set=data_set, segment=segment, form=upload_data_set_form)
    else:
        return render_template("home/data_set.html", data_set_details=data_set_details, data_set_field_names=data_set_field_names, data_set_display_field_details=data_set_display_field_details , segment=segment, form=edit_data_set_form)

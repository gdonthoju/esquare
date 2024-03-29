# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present kloudbee
"""

from typing import ItemsView
from apps.home import blueprint
from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required
from jinja2 import TemplateNotFound
from apps.authentication.models import kloudbeeDataSets, kloudbeeObservations, kloudbeeDataProducers, kloudbeeDataConsumers, kloudbeeDataSources, kloudbeeBusinessGlossary, kloudbeeDataCatalogue, kloudbeeDataSetFields
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
    search_query_form = SearchQueryForm(request.form)
    search_query = ''
    
    counts_data = {}
    counts_data['data_sources_count'] = kloudbeeDataSources.query.count()
    counts_data['business_glossary_count'] = kloudbeeBusinessGlossary.query.count()
    counts_data['data_catalogue_count'] = kloudbeeDataCatalogue.query.count()
    counts_data['hits_count'] = '#'
    counts_data['data_producers_count'] = kloudbeeDataProducers.query.count()
    counts_data['data_consumers_count'] = kloudbeeDataConsumers.query.count()
    counts_data['data_sets_count'] = kloudbeeDataSets.query.count()
    counts_data['data_observability_count'] = kloudbeeObservations.query.count()
    if request.method == 'GET' and 'search_query' in request.args.keys():
        search_query = request.args.get('search_query')
        print("Args : " , search_query)
        render_redirect = ''
        return redirect("search?search_query="+search_query)
    else:
        render_redirect = render_template('home/index.html', segment='index', counts_data = counts_data, form = universal_search_form, search_form=search_query_form, search_query=search_query)

    return render_redirect


@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        if template.startswith('notifications'):
            search_query_form = SearchQueryForm(request.form)
            search_query = ''

            if request.method == 'GET' and 'search_query' in request.args.keys():
                search_query = request.args.get('search_query')
                print("Args : " , search_query)
                observations = kloudbeeObservations.query.filter(or_(kloudbeeObservations.observation.contains(search_query)))
            else:
                observations = kloudbeeObservations.query.all()
            return render_template("home/" + template, observations=observations, segment=segment, search_form=search_query_form, search_query=search_query)

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


@blueprint.route('/data_sources', methods=['GET', 'POST'])
@login_required
def route_data_sources():
    # Detect the current page
    segment = get_segment(request)
    upload_data_sources_excel_form = UploadDataSourcesExcelForm(request.form)
    
    search_query_form = SearchQueryForm(request.form)
    search_query = ''

    if request.method == 'GET' and 'search_query' in request.args.keys():
        search_query = request.args.get('search_query')
        print("Args : " , search_query)
        data_sources = kloudbeeDataSources.query.filter(or_(kloudbeeDataSources.applicationName.contains(search_query),kloudbeeDataSources.description.contains(search_query)))
    else:
        data_sources = kloudbeeDataSources.query.all()

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
                dataSourceAdd = kloudbeeDataSources(**dataSourceExcelRowAdd)
                # print(dataProducerAdd)
                db.session.add(dataSourceAdd)
                db.session.commit()
                print(dataItem)
                # os.remove(UPLOAD_FOLDER + filename)
        return redirect("data_sources")
        # return render_template("home/data_sources.html", data_sources=data_sources, segment=segment, form=upload_data_sources_excel_form)
    else:
        return render_template("home/data_sources.html", data_sources=data_sources, segment=segment, form=upload_data_sources_excel_form, search_form=search_query_form, search_query=search_query)

@blueprint.route('/data_producers', methods=['GET', 'POST'])
@login_required
def route_data_producers():
    # Detect the current page
    segment = get_segment(request)
    upload_data_producers_excel_form = UploadDataProducersExcelForm(request.form)
    
    search_query_form = SearchQueryForm(request.form)
    search_query = ''

    if request.method == 'GET' and 'search_query' in request.args.keys():
        search_query = request.args.get('search_query')
        print("Args : " , search_query)
        data_producers = kloudbeeDataProducers.query.filter(or_(kloudbeeDataProducers.producerApplicationName.contains(search_query),kloudbeeDataProducers.description.contains(search_query)))
    else:
        data_producers = kloudbeeDataProducers.query.all()

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
                dataProducerAdd = kloudbeeDataProducers(**dataProducerExcelRowAdd)
                # print(dataProducerAdd)
                db.session.add(dataProducerAdd)
                db.session.commit()
                print(dataItem)
                # os.remove(UPLOAD_FOLDER + filename)
        return redirect("data_producers")
        # return render_template("home/data_producers.html", data_producers=data_producers, segment=segment, form=upload_data_producers_excel_form)
    else:
        return render_template("home/data_producers.html", data_producers=data_producers, segment=segment, form=upload_data_producers_excel_form ,search_form=search_query_form, search_query=search_query)

@blueprint.route('/data_consumers', methods=['GET', 'POST'])
@login_required
def route_data_consumers():
    # Detect the current page
    segment = get_segment(request)
    upload_data_consumers_excel_form = UploadDataConsumersExcelForm(request.form)
    
    search_query_form = SearchQueryForm(request.form)
    search_query = ''

    if request.method == 'GET' and 'search_query' in request.args.keys():
        search_query = request.args.get('search_query')
        print("Args : " , search_query)
        data_consumers = kloudbeeDataConsumers.query.filter(or_(kloudbeeDataConsumers.consumerApplicationName.contains(search_query),kloudbeeDataConsumers.description.contains(search_query)))
    else:
        data_consumers = kloudbeeDataConsumers.query.all()

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
                dataConsumerAdd = kloudbeeDataConsumers(**dataConsumerExcelRowAdd)
                print(dataConsumerExcelRowAdd)
                db.session.add(dataConsumerAdd)
                db.session.commit()
                print(dataItem)
        return redirect("data_consumers")
        # return render_template("home/data_producers.html", data_producers=data_producers, segment=segment, form=upload_data_producers_excel_form)
    else:
        return render_template("home/data_consumers.html", data_consumers=data_consumers, segment=segment, form=upload_data_consumers_excel_form ,search_form=search_query_form, search_query=search_query)

@blueprint.route('/business_glossary', methods=['GET', 'POST'])
@login_required
def route_business_glossary():
    # Detect the current page
    segment = get_segment(request)
    upload_business_glossary_excel_form = UploadBusinessGlossarysExcelForm(request.form)

    search_query_form = SearchQueryForm(request.form)
    search_query = ''

    if request.method == 'GET' and 'search_query' in request.args.keys():
        search_query = request.args.get('search_query')
        print("Args : " , search_query)
        business_glossary = kloudbeeBusinessGlossary.query.filter(or_(kloudbeeBusinessGlossary.businessDefinition.contains(search_query),kloudbeeBusinessGlossary.businessDomain.contains(search_query)))
    else:
        business_glossary = kloudbeeBusinessGlossary.query.all()

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
                businessGlossaryAdd = kloudbeeBusinessGlossary(**businessGlossaryExcelRowAdd)
                # print(dataProducerAdd)
                db.session.add(businessGlossaryAdd)
                db.session.commit()
                print(dataItem)
                # os.remove(UPLOAD_FOLDER + filename)
        return redirect("business_glossary")
        # return render_template("home/business_glossary.html", business_glossary=business_glossary, segment=segment, form=upload_business_glossary_excel_form)
    else:
        return render_template("home/business_glossary.html", business_glossary=business_glossary, segment=segment, form=upload_business_glossary_excel_form, search_form=search_query_form, search_query=search_query)

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
        data_catalogue = kloudbeeDataCatalogue.query.filter(or_(kloudbeeDataCatalogue.attributeName.contains(search_query),kloudbeeDataCatalogue.attributeDescription.contains(search_query)))
    else:
        data_catalogue = kloudbeeDataCatalogue.query.all()

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
                dataCatalogueAdd = kloudbeeDataCatalogue(**dataCatalogueExcelRowAdd)
                # print(dataProducerAdd)
                db.session.add(dataCatalogueAdd)
                db.session.commit()
                print(dataItem)
                # os.remove(UPLOAD_FOLDER + filename)
        return redirect("data_catalogue")
        # return render_template("home/data_catalogue.html", data_catalogue=data_catalogue, segment=segment, form=upload_data_catalogue_excel_form)
    else:
        return render_template("home/data_catalogue.html", data_catalogue=data_catalogue, segment=segment, form=upload_data_catalogue_excel_form, search_form=search_query_form, search_query=search_query)


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
        data_sets = kloudbeeDataSets.query.filter(or_(kloudbeeDataSets.dataSetName.contains(search_query),kloudbeeDataSets.dataSetDescription.contains(search_query)))
    else:
        data_sets = kloudbeeDataSets.query.all()
    
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

        dataSetAdd = kloudbeeDataSets(**dataSetValues)
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

                    dataSetFieldsAdd = kloudbeeDataSetFields(**dataSetExcelRowAdd)
                    db.session.add(dataSetFieldsAdd)
                    db.session.commit()
        return redirect("data_sets")
    else:
        return render_template("home/data_sets.html", data_sets=data_sets, segment=segment, form=upload_data_set_form, search_form=search_query_form, search_query=search_query)


@blueprint.route('/data_set/<data_set_id>', methods=['GET', 'POST'])
@login_required
def route_data_set(data_set_id):
    # Detect the current page
    segment = get_segment(request)
    edit_data_set_form = EditDataSetForm(request.form)
    data_set_field_names = kloudbeeDataSetFields.query.with_entities(kloudbeeDataSetFields.dataSetFieldName).filter_by(dataSetId=data_set_id).distinct()
    data_set_details = kloudbeeDataSets.query.filter_by(id=data_set_id)

    data_set_field_details_from_db = kloudbeeDataSetFields.query.filter_by(dataSetId=data_set_id)
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
        kloudbeeDataSetFields.query.filter_by(dataSetId=idDataSet).delete()
        db.session.commit()
        kloudbeeDataSets.query.filter_by(id=idDataSet).delete()
        db.session.commit()
        return redirect("data_sets")
        # return render_template("home/data_set.html", data_set=data_set, segment=segment, form=upload_data_set_form)
    else:
        return render_template("home/data_set.html", data_set_details=data_set_details, data_set_field_names=data_set_field_names, data_set_display_field_details=data_set_display_field_details , segment=segment, form=edit_data_set_form)

@blueprint.route('/search', methods=['GET', 'POST'])
@login_required
def route_search():
    # Detect the current page
    segment = get_segment(request)
    search_query_form = SearchQueryForm(request.form)
    search_query = ''

    if request.method == 'GET' and 'search_query' in request.args.keys():
        search_query = request.args.get('search_query')
        print("Args : " , search_query)
        data_sources_search = kloudbeeDataSources.query.filter(or_(kloudbeeDataSources.applicationName.contains(search_query),kloudbeeDataSources.description.contains(search_query)))
        data_producers_search = kloudbeeDataProducers.query.filter(or_(kloudbeeDataProducers.producerApplicationName.contains(search_query),kloudbeeDataProducers.description.contains(search_query)))
        data_consumers_search = kloudbeeDataConsumers.query.filter(or_(kloudbeeDataConsumers.consumerApplicationName.contains(search_query),kloudbeeDataConsumers.description.contains(search_query)))
        business_glossary_search = kloudbeeBusinessGlossary.query.filter(or_(kloudbeeBusinessGlossary.businessDefinition.contains(search_query),kloudbeeBusinessGlossary.businessDomain.contains(search_query)))
        data_catalogue_search = kloudbeeDataCatalogue.query.filter(or_(kloudbeeDataCatalogue.attributeName.contains(search_query),kloudbeeDataCatalogue.attributeDescription.contains(search_query)))
        data_sets_search = kloudbeeDataSets.query.filter(or_(kloudbeeDataSets.dataSetName.contains(search_query),kloudbeeDataSets.dataSetDescription.contains(search_query)))

        print("data_sources_search", data_sources_search)
        print("data_producers_search", data_producers_search)
        print("data_consumers_search", data_consumers_search)
        print("business_glossary_search", business_glossary_search)
        print("data_catalogue_search", data_catalogue_search)
        print("data_consumers_search", data_sets_search)
    
    # print("search : ", search)  

    return render_template("home/search.html", data_sources_search=data_sources_search, data_producers_search=data_producers_search, data_consumers_search=data_consumers_search, business_glossary_search=business_glossary_search, data_catalogue_search=data_catalogue_search, data_sets_search=data_sets_search, segment=segment, search_form=search_query_form, search_query=search_query)


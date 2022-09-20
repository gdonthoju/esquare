# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present kloudbee
"""
import datetime
from flask import render_template, redirect, request, url_for
from flask_login import (
    current_user,
    login_user,
    logout_user
)

from apps import db, login_manager
from apps.authentication import blueprint
from apps.authentication.forms import LoginForm, CreateAccountForm, CreateObservationForm, CreateDataProducerForm, CreateDataConsumerForm, EditDataProducerForm, CreateDataSourceForm, EditDataSourceForm, EditDataConsumerForm, CreateBusinessGlossaryForm, EditBusinessGlossaryForm, CreateDataCatalogueForm, EditDataCatalogueForm, CreateDataSetForm
from apps.authentication.models import Users, kloudbeeObservations, kloudbeeDataProducers, kloudbeeDataConsumers, kloudbeeDataSources, kloudbeeBusinessGlossary, kloudbeeDataCatalogue

from apps.authentication.util import verify_pass


@blueprint.route('/')
def route_default():
    return redirect(url_for('authentication_blueprint.login'))


# Login & Registration

@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    if 'login' in request.form:

        # read form data
        username = request.form['username']
        password = request.form['password']

        # Locate user
        user = Users.query.filter_by(username=username).first()

        # Check the password
        if user and verify_pass(password, user.password):

            login_user(user)
            return redirect(url_for('authentication_blueprint.route_default'))

        # Something (user or pass) is not ok
        return render_template('accounts/login.html',
                               msg='Wrong user or password',
                               form=login_form)

    if not current_user.is_authenticated:
        return render_template('accounts/login.html',
                               form=login_form)
    return redirect(url_for('home_blueprint.index'))


@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    create_account_form = CreateAccountForm(request.form)
    if 'register' in request.form:

        username = request.form['username']
        email = request.form['email']

        # Check usename exists
        user = Users.query.filter_by(username=username).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='Username already registered',
                                   success=False,
                                   form=create_account_form)

        # Check email exists
        user = Users.query.filter_by(email=email).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='Email already registered',
                                   success=False,
                                   form=create_account_form)

        # else we can create the user
        user = Users(**request.form)
        db.session.add(user)
        db.session.commit()

        return render_template('accounts/register.html',
                               msg='User created please <a href="/login">login</a>',
                               success=True,
                               form=create_account_form)

    else:
        return render_template('accounts/register.html', form=create_account_form)


@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('authentication_blueprint.login'))


# Errors

@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('home/page-404.html'), 404


@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('home/page-500.html'), 500


# Notifications or Data Observability

@blueprint.route('/observation-add', methods=['GET', 'POST'])
def observation_add():
    observation_add_form = CreateObservationForm(request.form)
    
    if 'add_observation' in request.form:

        # read form data
        observation_type = request.form['observation_type']
        observation = request.form['observation']

        # Check for observation - will be added later
        # user = Users.query.filter_by(username=username).first()
        # if user:
        #     return render_template('accounts/register.html',
        #                            msg='Username already registered',
        #                            success=False,
        #                            form=create_account_form)

        # # Check email exists
        # user = Users.query.filter_by(email=email).first()
        # if user:
        #     return render_template('accounts/register.html',
        #                            msg='Email already registered',
        #                            success=False,
        #                            form=create_account_form)

        # else we can create the user
        observation = kloudbeeObservations(**request.form)
        observation.observationOn = int(datetime.datetime.now().timestamp() * 1000)
        observation.observationBy = current_user.get_id()
        db.session.add(observation)
        db.session.commit()

        return render_template('accounts/observation-add.html',
                               msg='Observation added to kloudbee. please <a href="/notifications">view here</a>',
                               success=True,
                               form=observation_add_form)

    else:
        return render_template('accounts/observation-add.html', form=observation_add_form)

# Data Source

@blueprint.route('/data-source-add', methods=['GET', 'POST'])
def data_source_add():
    data_source_add_form = CreateDataSourceForm(request.form)
    if 'add_data_source' in request.form.keys():
        # read form data
        applicationName = request.form['applicationName']
        description = request.form['description']
        lineOfBusiness = request.form['lineOfBusiness']
        businessDomain = request.form['businessDomain']
        dataDomain = request.form['dataDomain']
        businessOwnerName = request.form['businessOwnerName']
        businessOwnerEmail = request.form['businessOwnerEmail']
        technicalOwnerName = request.form['technicalOwnerName']
        technicalOwnerEmail = request.form['technicalOwnerEmail']
        additionalInformation = request.form['additionalInformation']
        
        # Check for data-sourcing-add - will be added later
        # user = Users.query.filter_by(username=username).first()
        # if user:
        #     return render_template('accounts/register.html',
        #                            msg='Username already registered',
        #                            success=False,
        #                            form=create_account_form)

        # # Check email exists
        # user = Users.query.filter_by(email=email).first()
        # if user:
        #     return render_template('accounts/register.html',
        #                            msg='Email already registered',
        #                            success=False,
        #                            form=create_account_form)

        # else we can create the user
        dataSourceAdd = kloudbeeDataSources(**request.form)
        # print(dataSourceAdd)
        dataSourceAdd.dataSourceOn = int(datetime.datetime.now().timestamp() * 1000)
        dataSourceAdd.dataSourceBy = current_user.get_id()
        db.session.add(dataSourceAdd)
        db.session.commit()

        return render_template('accounts/data-source-add.html',
                               msg='Data Source added to kloudbee. please <a href="/data_sources">view here</a>',
                               success=True,
                               form=data_source_add_form)

    else:
        return render_template('accounts/data-source-add.html', form=data_source_add_form)


# Data Producer

@blueprint.route('/data-producer-add', methods=['GET', 'POST'])
def data_producer_add():
    data_producer_add_form = CreateDataProducerForm(request.form)
    if 'add_data_producer' in request.form.keys():
        # read form data
        applicationName = request.form['producerApplicationName']
        description = request.form['description']
        lineOfBusiness = request.form['lineOfBusiness']
        dataDomain = request.form['dataDomain']
        businessOwnerName = request.form['businessOwnerName']
        businessOwnerEmail = request.form['businessOwnerEmail']
        technicalOwnerName = request.form['technicalOwnerName']
        technicalOwnerEmail = request.form['technicalOwnerEmail']
        msg_batch_apis_name = request.form['msg_batch_apis_name']
        msg_batch_apis_description = request.form['msg_batch_apis_description']
        msg_batch_apis_type = request.form['msg_batch_apis_type']
        
        # Check for data-sourcing-add - will be added later
        # user = Users.query.filter_by(username=username).first()
        # if user:
        #     return render_template('accounts/register.html',
        #                            msg='Username already registered',
        #                            success=False,
        #                            form=create_account_form)

        # # Check email exists
        # user = Users.query.filter_by(email=email).first()
        # if user:
        #     return render_template('accounts/register.html',
        #                            msg='Email already registered',
        #                            success=False,
        #                            form=create_account_form)

        # else we can create the user
        dataProducerAdd = kloudbeeDataProducers(**request.form)
        # print(dataProducerAdd)
        dataProducerAdd.dataProducerOn = int(datetime.datetime.now().timestamp() * 1000)
        dataProducerAdd.dataProducerBy = current_user.get_id()
        db.session.add(dataProducerAdd)
        db.session.commit()

        return render_template('accounts/data-producer-add.html',
                               msg='Data Producer added to kloudbee. please <a href="/data_producers">view here</a>',
                               success=True,
                               form=data_producer_add_form)

    else:
        return render_template('accounts/data-producer-add.html', form=data_producer_add_form)

# Data Producer Edit

@blueprint.route('/data-producer-edit', methods=['GET', 'POST'])
def data_producer_edit():
    data_producer_edit_form = EditDataProducerForm(request.form)
    print("This is Firing" , request.form.keys())
    if 'edit_data_producer' in request.form.keys():
        # read form data
        idProducerApplication = request.form['id']
        applicationName = request.form['producerApplicationName']
        description = request.form['description']
        lineOfBusiness = request.form['lineOfBusiness']
        dataDomain = request.form['dataDomain']
        businessOwnerName = request.form['businessOwnerName']
        businessOwnerEmail = request.form['businessOwnerEmail']
        technicalOwnerName = request.form['technicalOwnerName']
        technicalOwnerEmail = request.form['technicalOwnerEmail']
        msg_batch_apis_name = request.form['msg_batch_apis_name']
        msg_batch_apis_description = request.form['msg_batch_apis_description']
        msg_batch_apis_type = request.form['msg_batch_apis_type']
        
        # Check for data-sourcing-edit - will be edited later
        # user = Users.query.filter_by(username=username).first()
        # if user:
        #     return render_template('accounts/register.html',
        #                            msg='Username already registered',
        #                            success=False,
        #                            form=create_account_form)

        # # Check email exists
        # user = Users.query.filter_by(email=email).first()
        # if user:
        #     return render_template('accounts/register.html',
        #                            msg='Email already registered',
        #                            success=False,
        #                            form=create_account_form)

        # else we can create the user
        dataProducerEdit = kloudbeeDataProducers(**request.form)
       
        updateData = dict(request.form)
        del updateData['csrf_token']
        del updateData['edit_data_producer']
        
        
        updateData['dataProducerOn'] = int(datetime.datetime.now().timestamp() * 1000)
        updateData['dataProducerBy'] = current_user.get_id()
        # print(updateData)
        kloudbeeDataProducers.query.filter_by(id=idProducerApplication).update(updateData)
        db.session.commit()

        return render_template('accounts/data-producer-edit.html',
                               msg='Data Producer edited to kloudbee. please <a href="/data_producers">view here</a>',
                               success=True,
                               form=data_producer_edit_form)

    elif 'delete_data_producer' in request.form.keys():
        idProducerApplication = request.form['id']
        print("delIdProducerApplication", idProducerApplication)
        kloudbeeDataProducers.query.filter_by(id=idProducerApplication).delete()
        db.session.commit()
        return redirect("data_producers")
    else:
        return render_template('accounts/data-producer-edit.html', form=data_producer_edit_form)

# Data Source Edit

@blueprint.route('/data-source-edit', methods=['GET', 'POST'])
def data_source_edit():
    data_source_edit_form = EditDataSourceForm(request.form)
    print("This is Firing" , request.form.keys())
    if 'edit_data_source' in request.form.keys():
        # read form data
        idSourceApplication = request.form['id']
        applicationName = request.form['applicationName']
        description = request.form['description']
        lineOfBusiness = request.form['lineOfBusiness']
        businessDomain = request.form['businessDomain']
        dataDomain = request.form['dataDomain']
        businessOwnerName = request.form['businessOwnerName']
        businessOwnerEmail = request.form['businessOwnerEmail']
        technicalOwnerName = request.form['technicalOwnerName']
        technicalOwnerEmail = request.form['technicalOwnerEmail']
        additionalInformation = request.form['additionalInformation']
        
        # Check for data-sourcing-edit - will be edited later
        # user = Users.query.filter_by(username=username).first()
        # if user:
        #     return render_template('accounts/register.html',
        #                            msg='Username already registered',
        #                            success=False,
        #                            form=create_account_form)

        # # Check email exists
        # user = Users.query.filter_by(email=email).first()
        # if user:
        #     return render_template('accounts/register.html',
        #                            msg='Email already registered',
        #                            success=False,
        #                            form=create_account_form)

        # else we can create the user
        dataSourceEdit = kloudbeeDataSources(**request.form)
       
        updateData = dict(request.form)
        del updateData['csrf_token']
        del updateData['edit_data_source']
        
        
        updateData['dataSourceOn'] = int(datetime.datetime.now().timestamp() * 1000)
        updateData['dataSourceBy'] = current_user.get_id()
        # print(updateData)
        kloudbeeDataSources.query.filter_by(id=idSourceApplication).update(updateData)
        db.session.commit()

        return render_template('accounts/data-source-edit.html',
                               msg='Data Source edited to kloudbee. please <a href="/data_sources">view here</a>',
                               success=True,
                               form=data_source_edit_form)

    elif 'delete_data_source' in request.form.keys():
        idSourceApplication = request.form['id']
        print("delIdSourceApplication", idSourceApplication)
        kloudbeeDataSources.query.filter_by(id=idSourceApplication).delete()
        db.session.commit()
        return redirect("data_sources")
    else:
        return render_template('accounts/data-source-edit.html', form=data_source_edit_form)


# Data Consumer

@blueprint.route('/data-consumer-add', methods=['GET', 'POST'])
def data_consumer_add():
    data_consumer_add_form = CreateDataConsumerForm(request.form)
    print("dataConsumerAdd is firing")
    if 'add_data_consumer' in request.form.keys():
        # read form data
        applicationName = request.form['consumerApplicationName']
        description = request.form['description']
        lineOfBusiness = request.form['lineOfBusiness']
        dataDomain = request.form['dataDomain']
        businessOwnerName = request.form['businessOwnerName']
        businessOwnerEmail = request.form['businessOwnerEmail']
        technicalOwnerName = request.form['technicalOwnerName']
        technicalOwnerEmail = request.form['technicalOwnerEmail']
        msg_batch_apis_name = request.form['msg_batch_apis_name']
        msg_batch_apis_description = request.form['msg_batch_apis_description']
        msg_batch_apis_type = request.form['msg_batch_apis_type']
        # Check for data-sourcing-add - will be added later
        # user = Users.query.filter_by(username=username).first()
        # if user:
        #     return render_template('accounts/register.html',
        #                            msg='Username already registered',
        #                            success=False,
        #                            form=create_account_form)

        # # Check email exists
        # user = Users.query.filter_by(email=email).first()
        # if user:
        #     return render_template('accounts/register.html',
        #                            msg='Email already registered',
        #                            success=False,
        #                            form=create_account_form)

        # else we can create the user
        dataConsumerAdd = kloudbeeDataConsumers(**request.form)
        # print(dataConsumerAdd)
        dataConsumerAdd.dataConsumerOn = int(datetime.datetime.now().timestamp() * 1000)
        dataConsumerAdd.dataConsumerBy = current_user.get_id()
        db.session.add(dataConsumerAdd)
        db.session.commit()

        return render_template('accounts/data-consumer-add.html',
                               msg='Data Consumer added to kloudbee. please <a href="/data_consumers">view here</a>',
                               success=True,
                               form=data_consumer_add_form)

    else:
        return render_template('accounts/data-consumer-add.html', form=data_consumer_add_form)

# Data Consumer Edit

@blueprint.route('/data-consumer-edit', methods=['GET', 'POST'])
def data_consumer_edit():
    data_consumer_edit_form = EditDataConsumerForm(request.form)
    print("This is Firing", request.form.keys())
    if 'edit_data_consumer' in request.form.keys():
        # read form data
        idConsumerApplication = request.form['id']
        applicationName = request.form['consumerApplicationName']
        description = request.form['description']
        lineOfBusiness = request.form['lineOfBusiness']
        dataDomain = request.form['dataDomain']
        businessOwnerName = request.form['businessOwnerName']
        businessOwnerEmail = request.form['businessOwnerEmail']
        technicalOwnerName = request.form['technicalOwnerName']
        technicalOwnerEmail = request.form['technicalOwnerEmail']
        msg_batch_apis_name = request.form['msg_batch_apis_name']
        msg_batch_apis_description = request.form['msg_batch_apis_description']
        msg_batch_apis_type = request.form['msg_batch_apis_type']

        # Check for data-sourcing-edit - will be edited later
        # user = Users.query.filter_by(username=username).first()
        # if user:
        #     return render_template('accounts/register.html',
        #                            msg='Username already registered',
        #                            success=False,
        #                            form=create_account_form)

        # # Check email exists
        # user = Users.query.filter_by(email=email).first()
        # if user:
        #     return render_template('accounts/register.html',
        #                            msg='Email already registered',
        #                            success=False,
        #                            form=create_account_form)

        # else we can create the user
        dataProducerEdit = kloudbeeDataProducers(**request.form)

        updateData = dict(request.form)
        del updateData['csrf_token']
        del updateData['edit_data_consumer']

        updateData['dataConsumerOn'] = int(datetime.datetime.now().timestamp() * 1000)
        updateData['dataConsumerBy'] = current_user.get_id()
        # print(updateData)
        kloudbeeDataConsumers.query.filter_by(id=idConsumerApplication).update(updateData)
        db.session.commit()

        return render_template('accounts/data-consumer-edit.html',
                               msg='Data Producer edited to kloudbee. please <a href="/data_consumers">view here</a>',
                               success=True,
                               form=data_consumer_edit_form)

    elif 'delete_data_consumer' in request.form.keys():
        idConsumerApplication = request.form['id']
        print("delIdProducerApplication", idConsumerApplication)
        kloudbeeDataConsumers.query.filter_by(id=idConsumerApplication).delete()
        db.session.commit()
        return redirect("data_consumers")
    else:
        return render_template('accounts/data-consumer-edit.html', form=data_consumer_edit_form)

# Business Glossary

@blueprint.route('/business-glossary-add', methods=['GET', 'POST'])
def business_glossary_add():
    business_glossary_add_form = CreateBusinessGlossaryForm(request.form)
    if 'add_business_glossary' in request.form.keys():
        # read form data
        businessGlossaryTerm = request.form['businessGlossaryTerm']
        businessDefinition = request.form['businessDefinition']
        businessDomain = request.form['businessDomain']
        termSource = request.form['termSource']
        dataDomain = request.form['dataDomain']
        businessSteward = request.form['businessSteward']
        
        # Check for data-sourcing-add - will be added later
        # user = Users.query.filter_by(username=username).first()
        # if user:
        #     return render_template('accounts/register.html',
        #                            msg='Username already registered',
        #                            success=False,
        #                            form=create_account_form)

        # # Check email exists
        # user = Users.query.filter_by(email=email).first()
        # if user:
        #     return render_template('accounts/register.html',
        #                            msg='Email already registered',
        #                            success=False,
        #                            form=create_account_form)

        # else we can create the user
        businessGlossaryAdd = kloudbeeBusinessGlossary(**request.form)
        # print(businessGlossaryAdd)
        businessGlossaryAdd.businessGlossaryOn = int(datetime.datetime.now().timestamp() * 1000)
        businessGlossaryAdd.businessGlossaryBy = current_user.get_id()
        db.session.add(businessGlossaryAdd)
        db.session.commit()

        return render_template('accounts/business-glossary-add.html',
                               msg='Business Glossary added to kloudbee. please <a href="/business_glossary">view here</a>',
                               success=True,
                               form=business_glossary_add_form)

    else:
        return render_template('accounts/business-glossary-add.html', form=business_glossary_add_form)


# Business Glossary Edit

@blueprint.route('/business-glossary-edit', methods=['GET', 'POST'])
def business_glossary_edit():
    business_glossary_edit_form = EditBusinessGlossaryForm(request.form)
    print("This is Firing" , request.form.keys())
    if 'edit_business_glossary' in request.form.keys():
        # read form data
        idBusinessGlossary = request.form['id']
        businessGlossaryTerm = request.form['businessGlossaryTerm']
        businessDefinition = request.form['businessDefinition']
        businessDomain = request.form['businessDomain']
        termSource = request.form['termSource']
        dataDomain = request.form['dataDomain']
        businessSteward = request.form['businessSteward']
        
        # Check for data-sourcing-edit - will be edited later
        # user = Users.query.filter_by(username=username).first()
        # if user:
        #     return render_template('accounts/register.html',
        #                            msg='Username already registered',
        #                            success=False,
        #                            form=create_account_form)

        # # Check email exists
        # user = Users.query.filter_by(email=email).first()
        # if user:
        #     return render_template('accounts/register.html',
        #                            msg='Email already registered',
        #                            success=False,
        #                            form=create_account_form)

        # else we can create the user
        businessGlossaryEdit = kloudbeeBusinessGlossary(**request.form)
       
        updateData = dict(request.form)
        del updateData['csrf_token']
        del updateData['edit_business_glossary']
        
        
        updateData['businessGlossaryOn'] = int(datetime.datetime.now().timestamp() * 1000)
        updateData['businessGlossaryBy'] = current_user.get_id()
        # print(updateData)
        kloudbeeBusinessGlossary.query.filter_by(id=idBusinessGlossary).update(updateData)
        db.session.commit()

        return render_template('accounts/business-glossary-edit.html',
                               msg='Business Glossary edited to kloudbee. please <a href="/business_glossary">view here</a>',
                               success=True,
                               form=business_glossary_edit_form)

    elif 'delete_business_glossary' in request.form.keys():
        idBusinessGlossary = request.form['id']
        print("delIdBusinessGlossary", idBusinessGlossary)
        kloudbeeBusinessGlossary.query.filter_by(id=idBusinessGlossary).delete()
        db.session.commit()
        return redirect("business_glossary")
    else:
        return render_template('accounts/business-glossary-edit.html', form=business_glossary_edit_form)

# Data Catalogue

@blueprint.route('/data-catalogue-add', methods=['GET', 'POST'])
def data_catalogue_add():
    data_catalogue_add_form = CreateDataCatalogueForm(request.form)
    if 'add_data_catalogue' in request.form.keys():
        # read form data
        attributeName = request.form['attributeName']
        attributeDescription = request.form['attributeDescription']
        tableName = request.form['tableName']
        columnName = request.form['columnName']
        columnDescription = request.form['columnDescription']
        columnDatatype = request.form['columnDatatype']
        isNullable = request.form['isNullable']
        isPrimaryKey = request.form['isPrimaryKey']
        isForeignKey = request.form['isForeignKey']
        attributeSensitivity = request.form['attributeSensitivity']
        termSource = request.form['termSource']
        possibleValues = request.form['possibleValues']
        valuesDescription = request.form['valuesDescription']
        notes = request.form['notes']
        
        # Check for data-sourcing-add - will be added later
        # user = Users.query.filter_by(username=username).first()
        # if user:
        #     return render_template('accounts/register.html',
        #                            msg='Username already registered',
        #                            success=False,
        #                            form=create_account_form)

        # # Check email exists
        # user = Users.query.filter_by(email=email).first()
        # if user:
        #     return render_template('accounts/register.html',
        #                            msg='Email already registered',
        #                            success=False,
        #                            form=create_account_form)

        # else we can create the user
        dataCatalogueAdd = kloudbeeDataCatalogue(**request.form)
        # print(dataCatalogueAdd)
        dataCatalogueAdd.catalogueAttributeCreatedOn = int(datetime.datetime.now().timestamp() * 1000)
        dataCatalogueAdd.catalogueAttributeCreatedBy = current_user.get_id()
        dataCatalogueAdd.catalogueAttributeUpdatedBy = current_user.get_id()
        db.session.add(dataCatalogueAdd)
        db.session.commit()

        return render_template('accounts/data-catalogue-add.html',
                               msg='Data Catalogue Attribute added to kloudbee. please <a href="/data_catalogue">view here</a>',
                               success=True,
                               form=data_catalogue_add_form)

    else:
        return render_template('accounts/data-catalogue-add.html', form=data_catalogue_add_form)


# Data Catalogue Edit

@blueprint.route('/data-catalogue-edit', methods=['GET', 'POST'])
def data_catalogue_edit():
    data_catalogue_edit_form = EditDataCatalogueForm(request.form)
    print("This is Firing" , request.form.keys())
    if 'edit_data_catalogue' in request.form.keys():
        # read form data
        idDataCatalogue = request.form['id']
        attributeName = request.form['attributeName']
        attributeDescription = request.form['attributeDescription']
        tableName = request.form['tableName']
        columnName = request.form['columnName']
        columnDescription = request.form['columnDescription']
        columnDatatype = request.form['columnDatatype']
        isNullable = request.form['isNullable']
        isPrimaryKey = request.form['isPrimaryKey']
        isForeignKey = request.form['isForeignKey']
        attributeSensitivity = request.form['attributeSensitivity']
        termSource = request.form['termSource']
        possibleValues = request.form['possibleValues']
        valuesDescription = request.form['valuesDescription']
        notes = request.form['notes']
        
        # Check for data-sourcing-edit - will be edited later
        # user = Users.query.filter_by(username=username).first()
        # if user:
        #     return render_template('accounts/register.html',
        #                            msg='Username already registered',
        #                            success=False,
        #                            form=create_account_form)

        # # Check email exists
        # user = Users.query.filter_by(email=email).first()
        # if user:
        #     return render_template('accounts/register.html',
        #                            msg='Email already registered',
        #                            success=False,
        #                            form=create_account_form)

        # else we can create the user
        dataCatalogueEdit = kloudbeeDataCatalogue(**request.form)
       
        updateData = dict(request.form)
        del updateData['csrf_token']
        del updateData['edit_data_catalogue']
        
        
        updateData['catalogueAttributeCreatedOn'] = int(datetime.datetime.now().timestamp() * 1000)
        updateData['catalogueAttributeUpdatedBy'] = current_user.get_id()
        # print(updateData)
        kloudbeeDataCatalogue.query.filter_by(id=idDataCatalogue).update(updateData)
        db.session.commit()

        return render_template('accounts/data-catalogue-edit.html',
                               msg='Data Catalogue edited to kloudbee. please <a href="/data_catalogue">view here</a>',
                               success=True,
                               form=data_catalogue_edit_form)

    elif 'delete_data_catalogue' in request.form.keys():
        idDataCatalogue = request.form['id']
        print("delIdDataCatalogue", idDataCatalogue)
        kloudbeeDataCatalogue.query.filter_by(id=idDataCatalogue).delete()
        db.session.commit()
        return redirect("data_catalogue")
    else:
        return render_template('accounts/data-catalogue-edit.html', form=data_catalogue_edit_form)
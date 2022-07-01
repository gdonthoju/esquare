# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
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
from apps.authentication.forms import LoginForm, CreateAccountForm, CreateObservationForm, CreateDataProducerForm, CreateDataConsumerForm, EditDataProducerForm, CreateDataSourceForm, EditDataSourceForm
from apps.authentication.models import Users, eSquareObservations, eSquareDataProducers, eSquareDataConsumers, eSquareDataSources

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
        observation = eSquareObservations(**request.form)
        observation.observationOn = int(datetime.datetime.now().timestamp() * 1000)
        observation.observationBy = current_user.get_id()
        db.session.add(observation)
        db.session.commit()

        return render_template('accounts/observation-add.html',
                               msg='Observation added to eSquare. please <a href="/notifications">view here</a>',
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
        dataSourceAdd = eSquareDataSources(**request.form)
        # print(dataSourceAdd)
        dataSourceAdd.dataSourceOn = int(datetime.datetime.now().timestamp() * 1000)
        dataSourceAdd.dataSourceBy = current_user.get_id()
        db.session.add(dataSourceAdd)
        db.session.commit()

        return render_template('accounts/data-source-add.html',
                               msg='Data Source added to eSquare. please <a href="/data_sources">view here</a>',
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
        dataProducerAdd = eSquareDataProducers(**request.form)
        # print(dataProducerAdd)
        dataProducerAdd.dataProducerOn = int(datetime.datetime.now().timestamp() * 1000)
        dataProducerAdd.dataProducerBy = current_user.get_id()
        db.session.add(dataProducerAdd)
        db.session.commit()

        return render_template('accounts/data-producer-add.html',
                               msg='Data Producer added to eSquare. please <a href="/data_producers">view here</a>',
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
        dataProducerEdit = eSquareDataProducers(**request.form)
       
        updateData = dict(request.form)
        del updateData['csrf_token']
        del updateData['edit_data_producer']
        
        
        updateData['dataProducerOn'] = int(datetime.datetime.now().timestamp() * 1000)
        updateData['dataProducerBy'] = current_user.get_id()
        # print(updateData)
        eSquareDataProducers.query.filter_by(id=idProducerApplication).update(updateData)
        db.session.commit()

        return render_template('accounts/data-producer-edit.html',
                               msg='Data Producer edited to eSquare. please <a href="/data_producers">view here</a>',
                               success=True,
                               form=data_producer_edit_form)

    elif 'delete_data_producer' in request.form.keys():
        idProducerApplication = request.form['id']
        print("delIdProducerApplication", idProducerApplication)
        eSquareDataProducers.query.filter_by(id=idProducerApplication).delete()
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
        dataSourceEdit = eSquareDataSources(**request.form)
       
        updateData = dict(request.form)
        del updateData['csrf_token']
        del updateData['edit_data_source']
        
        
        updateData['dataSourceOn'] = int(datetime.datetime.now().timestamp() * 1000)
        updateData['dataSourceBy'] = current_user.get_id()
        # print(updateData)
        eSquareDataSources.query.filter_by(id=idSourceApplication).update(updateData)
        db.session.commit()

        return render_template('accounts/data-source-edit.html',
                               msg='Data Source edited to eSquare. please <a href="/data_sources">view here</a>',
                               success=True,
                               form=data_source_edit_form)

    elif 'delete_data_source' in request.form.keys():
        idSourceApplication = request.form['id']
        print("delIdSourceApplication", idSourceApplication)
        eSquareDataSources.query.filter_by(id=idSourceApplication).delete()
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
        dataConsumerAdd = eSquareDataConsumers(**request.form)
        # print(dataConsumerAdd)
        dataConsumerAdd.dataConsumerOn = int(datetime.datetime.now().timestamp() * 1000)
        dataConsumerAdd.dataConsumerBy = current_user.get_id()
        db.session.add(dataConsumerAdd)
        db.session.commit()

        return render_template('accounts/data-consumer-add.html',
                               msg='Data Consumer added to eSquare. please <a href="/data_consumers">view here</a>',
                               success=True,
                               form=data_consumer_add_form)

    else:
        return render_template('accounts/data-consumer-add.html', form=data_consumer_add_form)

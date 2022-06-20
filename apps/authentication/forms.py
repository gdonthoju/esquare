# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from importlib.resources import contents
from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, TextAreaField, SelectField
from wtforms.validators import Email, DataRequired

# login and registration


class LoginForm(FlaskForm):
    username = TextField('Username',
                         id='username_login',
                         validators=[DataRequired()])
    password = PasswordField('Password',
                             id='pwd_login',
                             validators=[DataRequired()])


class CreateAccountForm(FlaskForm):
    username = TextField('Username',
                         id='username_create',
                         validators=[DataRequired()])
    email = TextField('Email',
                      id='email_create',
                      validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             id='pwd_create',
                             validators=[DataRequired()])

class CreateObservationForm(FlaskForm):
    observation_type = SelectField('Type',
                      choices=[('primary', 'Primary'), ('secondary', 'Secondary'), ('success', 'Success'), ('danger', 'Danger'), ('warning', 'Warning'), ('info', 'Info')],
                      id='observation_type',
                      validators=[DataRequired()])
    observation = TextAreaField('Observation',
                         id='observation',
                         render_kw={'class': 'form-control', 'rows': 5},
                         validators=[DataRequired()])
    
class CreateDataProducerForm(FlaskForm):
    producerApplicationName = TextField('Producing Application Name',
                         id='producerApplicationName',
                         validators=[DataRequired()])
    description = TextAreaField('Description',
                         id='description',
                         render_kw={'class': 'form-control', 'rows': 5},
                         validators=[DataRequired()])
    lineOfBusiness = TextField('Line of Business',
                         id='lineOfBusiness',
                         validators=[DataRequired()])
    dataDomain = TextField('Data Domain',
                         id='dataDomain',
                         validators=[DataRequired()])
    businessOwnerName = TextField('Business Owner Name',
                         id='businessOwnerName',
                         validators=[DataRequired()])
    businessOwnerEmail = TextField('Business Owner Email',
                         id='businessOwnerEmail',
                         validators=[DataRequired(), Email()])
    technicalOwnerName = TextField('Technical Owner Name',
                         id='technicalOwnerName',
                         validators=[DataRequired()])
    technicalOwnerEmail = TextField('Technical Owner Email',
                         id='technicalOwnerEmail',
                         validators=[DataRequired(), Email()])
    msg_batch_apis_name = TextField('Name (Msg/Batch/APIs)',
                         id='msg_batch_apis_name',
                         validators=[DataRequired()])
    msg_batch_apis_description = TextField('Description (Msg/Batch/APIs)',
                         id='msg_batch_apis_description',
                         validators=[DataRequired()])
    msg_batch_apis_type = TextField('Type (Msg/Batch/APIs)',
                         id='msg_batch_apis_type',
                         validators=[DataRequired()])

class CreateDataConsumerForm(FlaskForm):
    consumerApplicationName = TextField('Consumers Application Name',
                         id='consumerApplicationName',
                         validators=[DataRequired()])
    description = TextAreaField('Description',
                         id='description',
                         render_kw={'class': 'form-control', 'rows': 5},
                         validators=[DataRequired()])
    lineOfBusiness = TextField('Line of Business',
                         id='lineOfBusiness',
                         validators=[DataRequired()])
    dataDomain = TextField('Data Domain',
                         id='dataDomain',
                         validators=[DataRequired()])
    businessOwnerName = TextField('Business Owner Name',
                         id='businessOwnerName',
                         validators=[DataRequired()])
    businessOwnerEmail = TextField('Business Owner Email',
                         id='businessOwnerEmail',
                         validators=[DataRequired(), Email()])
    technicalOwnerName = TextField('Technical Owner Name',
                         id='technicalOwnerName',
                         validators=[DataRequired()])
    technicalOwnerEmail = TextField('Technical Owner Email',
                         id='technicalOwnerEmail',
                         validators=[DataRequired(), Email()])
    msg_batch_apis_name = TextField('Name (Msg/Batch/APIs)',
                         id='msg_batch_apis_name',
                         validators=[DataRequired()])
    msg_batch_apis_description = TextField('Description (Msg/Batch/APIs)',
                         id='msg_batch_apis_description',
                         validators=[DataRequired()])
    msg_batch_apis_type = TextField('Type (Msg/Batch/APIs)',
                         id='msg_batch_apis_type',
                         validators=[DataRequired()])

class CreateDataSourceForm(FlaskForm):
    applicationName = TextField('Data Source Name',
                         id='applicationName',
                         validators=[DataRequired()])
    description = TextAreaField('Description',
                         id='description',
                         render_kw={'class': 'form-control', 'rows': 5},
                         validators=[DataRequired()])
    lineOfBusiness = TextField('Line of Business',
                         id='lineOfBusiness',
                         validators=[DataRequired()])
    businessDomain = TextField('Business Domain',
                         id='businessDomain',
                         validators=[DataRequired()])
    dataDomain = TextField('Data Domain',
                         id='dataDomain',
                         validators=[DataRequired()])
    businessOwnerName = TextField('Business Owner Name',
                         id='businessOwnerName',
                         validators=[DataRequired()])
    businessOwnerEmail = TextField('Business Owner Email',
                         id='businessOwnerEmail',
                         validators=[DataRequired(), Email()])
    technicalOwnerName = TextField('Technical Owner Name',
                         id='technicalOwnerName',
                         validators=[DataRequired()])
    technicalOwnerEmail = TextField('Technical Owner Email',
                         id='technicalOwnerEmail',
                         validators=[DataRequired(), Email()])
    additionalInformation = TextField('Additional Information',
                         id='additionalInformation',
                         validators=[DataRequired()])

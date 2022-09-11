# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present eSquare
"""

from email.policy import default
from importlib.resources import contents
from wsgiref.validate import validator
from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, TextAreaField, SelectField, HiddenField, FileField, BooleanField
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

class UniversalSearchForm(FlaskForm):
    universalSearchField = TextField('Search',
                         id='universalSearchField',
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
    msg_batch_apis_description = TextAreaField('Description (Msg/Batch/APIs)',
                         id='msg_batch_apis_description',
                         render_kw={'class': 'form-control', 'rows': 5},
                         validators=[DataRequired()])
    msg_batch_apis_type = TextField('Type (Msg/Batch/APIs)',
                         id='msg_batch_apis_type',
                         validators=[DataRequired()])

class UploadDataProducersExcelForm(FlaskForm):
    excelFilePath = FileField('Excel File Path',
                         id='excelFilePath',
                         validators=[DataRequired()])

class EditDataProducerForm(FlaskForm):
    id = HiddenField('id',id='id')
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
    msg_batch_apis_description = TextAreaField('Description (Msg/Batch/APIs)',
                         id='msg_batch_apis_description',
                         render_kw={'class': 'form-control', 'rows': 5},
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
    msg_batch_apis_description = TextAreaField('Description (Msg/Batch/APIs)',
                         id='msg_batch_apis_description',
                         render_kw={'class': 'form-control', 'rows': 5},
                         validators=[DataRequired()])
    msg_batch_apis_type = TextField('Type (Msg/Batch/APIs)',
                         id='msg_batch_apis_type',
                         validators=[DataRequired()])

class UploadDataConsumersExcelForm(FlaskForm):
    excelFilePath = FileField('Excel File Path',
                         id='excelFilePath',
                         validators=[DataRequired()])

class EditDataConsumerForm(FlaskForm):
    id = HiddenField('id',id='id')
    consumerApplicationName = TextField('Consumer Application Name',
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
    msg_batch_apis_description = TextAreaField('Description (Msg/Batch/APIs)',
                         id='msg_batch_apis_description',
                         render_kw={'class': 'form-control', 'rows': 5},
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
    additionalInformation = TextAreaField('Additional Information',
                         id='additionalInformation',
                         render_kw={'class': 'form-control', 'rows': 5},
                         validators=[DataRequired()])

class UploadDataSourcesExcelForm(FlaskForm):
    excelFilePath = FileField('Excel File Path',
                         id='excelFilePath',
                         validators=[DataRequired()])

class EditDataSourceForm(FlaskForm):
    id = HiddenField('id',id='id')
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
    additionalInformation = TextAreaField('Additional Information',
                         id='additionalInformation',
                         render_kw={'class': 'form-control', 'rows': 5},
                         validators=[DataRequired()])

class CreateBusinessGlossaryForm(FlaskForm):
    businessGlossaryTerm = TextField('Business Glossary Term',
                         id='businessGlossaryTerm',
                         validators=[DataRequired()])
    businessDefinition = TextAreaField('Business Definition',
                         id='businessDefinition',
                         render_kw={'class': 'form-control', 'rows': 5},
                         validators=[DataRequired()])
    businessDomain = TextField('Business Domain',
                         id='businessDomain',
                         validators=[DataRequired()])
    termSource = TextField('Term Source',
                         id='termSource',
                         validators=[DataRequired()])
    dataDomain = TextField('Data Domain',
                         id='dataDomain',
                         validators=[DataRequired()])
    businessSteward = TextField('Business Steward',
                         id='businessSteward',
                         validators=[DataRequired()])

class UploadBusinessGlossarysExcelForm(FlaskForm):
    excelFilePath = FileField('Excel File Path',
                         id='excelFilePath',
                         validators=[DataRequired()])

class EditBusinessGlossaryForm(FlaskForm):
    id = HiddenField('id',id='id')
    businessGlossaryTerm = TextField('Business Glossary Term',
                         id='businessGlossaryTerm',
                         validators=[DataRequired()])
    businessDefinition = TextAreaField('Business Definition',
                         id='businessDefinition',
                         render_kw={'class': 'form-control', 'rows': 5},
                         validators=[DataRequired()])
    businessDomain = TextField('Business Domain',
                         id='businessDomain',
                         validators=[DataRequired()])
    termSource = TextField('Term Source',
                         id='termSource',
                         validators=[DataRequired()])
    dataDomain = TextField('Data Domain',
                         id='dataDomain',
                         validators=[DataRequired()])
    businessSteward = TextField('Business Steward',
                         id='businessSteward',
                         validators=[DataRequired()])

class CreateDataCatalogueForm(FlaskForm):
    attributeName = TextField('Attribute Name',
                         id='attributeName',
                         validators=[DataRequired()])
    attributeDescription = TextAreaField('Attribute Description',
                         id='attributeDescription',
                         render_kw={'class': 'form-control', 'rows': 5},
                         validators=[DataRequired()])
    tableName = TextField('Table Name',
                         id='tableName',
                         validators=[DataRequired()])
    columnName = TextField('Column Name',
                         id='columnName',
                         validators=[DataRequired()])
    columnDescription = TextAreaField('Column Description',
                         id='columnDescription',
                         render_kw={'class': 'form-control', 'rows': 5},
                         validators=[DataRequired()])
    columnDatatype = SelectField('Column Datatype',
                      choices=[('INT', 'INT'), ('CHAR', 'CHAR'), ('DATE', 'DATE')],
                      id='columnDatatype',
                      validators=[DataRequired()])
    isNullable = SelectField('Is Nullable',
                      choices=[(0, 'No'), (1, 'Yes')],
                      id='isNullable',
                      validators=[DataRequired()])
    isPrimaryKey = SelectField('Is Primary Key',
                      choices=[(0, 'No'), (1, 'Yes')],
                      id='isPrimaryKey',
                      validators=[DataRequired()])
    isForeignKey = SelectField('Is Foreign Key',
                      choices=[(0, 'No'), (1, 'Yes')],
                      id='isForeignKey',
                      validators=[DataRequired()])
    attributeSensitivity = TextField('Attribute Sensitivity',
                         id='attributeSensitivity',
                         validators=[])
    termSource = TextField('Term Source',
                         id='termSource',
                         validators=[DataRequired()])
    possibleValues = TextAreaField('Possible Values',
                         id='possibleValues',
                         render_kw={'class': 'form-control', 'rows': 5, 'placeholder':'Provide pipe(|) delimited for multiple values'},
                         validators=[DataRequired()])
    valuesDescription = TextAreaField('Values Description',
                         id='valuesDescription',
                         render_kw={'class': 'form-control', 'rows': 5, 'placeholder':'Provide pipe(|) delimited for multiple values corresponding to possible values'},
                         validators=[])
    notes = TextAreaField('Notes',
                         id='notes',
                         render_kw={'class': 'form-control', 'rows': 5},
                         validators=[DataRequired()])

class UploadDataCataloguesExcelForm(FlaskForm):
    excelFilePath = FileField('Excel File Path',
                         id='excelFilePath',
                         validators=[DataRequired()])

class EditDataCatalogueForm(FlaskForm):
    id = HiddenField('id',id='id')
    attributeName = TextField('Attribute Name',
                         id='attributeName',
                         validators=[DataRequired()])
    attributeDescription = TextAreaField('Attribute Description',
                         id='attributeDescription',
                         render_kw={'class': 'form-control', 'rows': 5},
                         validators=[DataRequired()])
    tableName = TextField('Table Name',
                         id='tableName',
                         validators=[DataRequired()])
    columnName = TextField('Column Name',
                         id='columnName',
                         validators=[DataRequired()])
    columnDescription = TextAreaField('Column Description',
                         id='columnDescription',
                         render_kw={'class': 'form-control', 'rows': 5},
                         validators=[DataRequired()])
    columnDatatype = SelectField('Column Datatype',
                      choices=[('INT', 'INT'), ('CHAR', 'CHAR'), ('DATE', 'DATE')],
                      id='columnDatatype',
                      validators=[DataRequired()])
    isNullable = SelectField('Is Nullable',
                      choices=[(0, 'No'), (1, 'Yes')],
                      id='isNullable',
                      validators=[DataRequired()])
    isPrimaryKey = SelectField('Is Primary Key',
                      choices=[(0, 'No'), (1, 'Yes')],
                      id='isPrimaryKey',
                      validators=[DataRequired()])
    isForeignKey = SelectField('Is Foreign Key',
                      choices=[(0, 'No'), (1, 'Yes')],
                      id='isForeignKey',
                      validators=[DataRequired()])
    attributeSensitivity = TextField('Attribute Sensitivity',
                         id='attributeSensitivity',
                         validators=[])
    termSource = TextField('Term Source',
                         id='termSource',
                         validators=[DataRequired()])
    possibleValues = TextAreaField('Possible Values',
                         id='possibleValues',
                         render_kw={'class': 'form-control', 'rows': 5, 'placeholder':'Provide pipe(|) delimited for multiple values'},
                         validators=[DataRequired()])
    valuesDescription = TextAreaField('Values Description',
                         id='valuesDescription',
                         render_kw={'class': 'form-control', 'rows': 5, 'placeholder':'Provide pipe(|) delimited for multiple values corresponding to possible values'},
                         validators=[])
    notes = TextAreaField('Notes',
                         id='notes',
                         render_kw={'class': 'form-control', 'rows': 5},
                         validators=[DataRequired()])
                         
class CreateDataSetForm(FlaskForm):
    dataSetName = TextField('Data Set Name',
                         id='dataSetName',
                         validators=[DataRequired()])
    dataSetDescription = TextAreaField('Data Set Description',
                         id='dataSetDescription',
                         render_kw={'class': 'form-control', 'rows': 5},
                         validators=[DataRequired()])
    excelFilePath = FileField('Excel File Path',
                         id='excelFilePath',
                         validators=[DataRequired()])
    
class EditDataSetForm(FlaskForm):
    id = HiddenField('id',id='id')
    dataSetName = TextField('Data Set Name',
                         id='dataSetName',
                         validators=[DataRequired()])
    dataSetDescription = TextAreaField('Data Set Description',
                         id='dataSetDescription',
                         render_kw={'class': 'form-control', 'rows': 5},
                         validators=[DataRequired()])

class UploadDataSetElementsExcelForm(FlaskForm):
    excelFilePath = FileField('Excel File Path',
                         id='excelFilePath',
                         validators=[DataRequired()])
                         
class CreateDataDomainForm(FlaskForm):
    dataDomain = TextField('Data Domain',
                         id='dataDomain',
                         validators=[DataRequired()])
    dataDomainDescription = TextAreaField('Data Domain Description',
                         id='dataDomainDescription',
                         render_kw={'class': 'form-control', 'rows': 5},
                         validators=[DataRequired()])

class UploadDataDomainsExcelForm(FlaskForm):
    excelFilePath = FileField('Excel File Path',
                         id='excelFilePath',
                         validators=[DataRequired()])

class EditDataDomainForm(FlaskForm):
    id = HiddenField('id',id='id')
    dataDomain = TextField('Data Domain',
                         id='dataDomain',
                         validators=[DataRequired()])
    dataDomainDescription = TextAreaField('Data Domain Description',
                         id='dataDomainDescription',
                         render_kw={'class': 'form-control', 'rows': 5},
                         validators=[DataRequired()])

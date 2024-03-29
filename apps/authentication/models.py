# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present kloudbee
"""

from flask_login import UserMixin

from apps import db, login_manager

from apps.authentication.util import hash_pass

class Users(db.Model, UserMixin):

    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.LargeBinary)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            if property == 'password':
                value = hash_pass(value)  # we need bytes here (not plain str)

            setattr(self, property, value)

    def __repr__(self):
        return str(self.username)


@login_manager.user_loader
def user_loader(id):
    return Users.query.filter_by(id=id).first()


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = Users.query.filter_by(username=username).first()
    return user if user else None


class kloudbeeObservations(db.Model):

    __tablename__ = 'kloudbeeObservations'

    id = db.Column(db.Integer, primary_key=True)
    observation = db.Column(db.String(1024))
    observation_type = db.Column(db.String(64))
    observationOn = db.Column(db.String(64), unique=True)
    observationBy = db.Column(db.Integer)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            setattr(self, property, value)

    def __repr__(self):
        return str(self.observation)

class kloudbeeDataSources(db.Model):

    __tablename__ = 'kloudbeeDataSources'

    id = db.Column(db.Integer, primary_key=True)
    applicationName = db.Column(db.String(255))
    description = db.Column(db.String(1024))
    lineOfBusiness = db.Column(db.String(255))
    businessDomain = db.Column(db.String(255))
    dataDomain = db.Column(db.String(255))
    businessOwnerName = db.Column(db.String(255))
    businessOwnerEmail = db.Column(db.String(255))
    technicalOwnerName = db.Column(db.String(255))
    technicalOwnerEmail = db.Column(db.String(255))
    additionalInformation = db.Column(db.String(1024))
    dataSourceOn = db.Column(db.String(64), unique=True)
    dataSourceBy = db.Column(db.Integer)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            setattr(self, property, value)

    def __repr__(self):
        return str(self.applicationName)

class kloudbeeDataConsumers(db.Model):

    __tablename__ = 'kloudbeeDataConsumers'

    id = db.Column(db.Integer, primary_key=True)
    consumerApplicationName = db.Column(db.String(255))
    description = db.Column(db.String(1024))
    lineOfBusiness = db.Column(db.String(255))
    dataDomain = db.Column(db.String(255))
    businessOwnerName = db.Column(db.String(255))
    businessOwnerEmail = db.Column(db.String(255))
    technicalOwnerName = db.Column(db.String(255))
    technicalOwnerEmail = db.Column(db.String(255))
    msg_batch_apis_name = db.Column(db.String(255))
    msg_batch_apis_description = db.Column(db.String(1024))
    msg_batch_apis_type = db.Column(db.String(255))
    dataConsumerOn = db.Column(db.String(64))
    dataConsumerBy = db.Column(db.Integer)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            setattr(self, property, value)

    def __repr__(self):
        return str(self.consumerApplicationName)

class kloudbeeDataProducers(db.Model):

    __tablename__ = 'kloudbeeDataProducers'

    id = db.Column(db.Integer, primary_key=True)
    producerApplicationName = db.Column(db.String(255))
    description = db.Column(db.String(1024))
    lineOfBusiness = db.Column(db.String(255))
    dataDomain = db.Column(db.String(255))
    businessOwnerName = db.Column(db.String(255))
    businessOwnerEmail = db.Column(db.String(255))
    technicalOwnerName = db.Column(db.String(255))
    technicalOwnerEmail = db.Column(db.String(255))
    msg_batch_apis_name = db.Column(db.String(255))
    msg_batch_apis_description = db.Column(db.String(1024))
    msg_batch_apis_type = db.Column(db.String(255))
    dataProducerOn = db.Column(db.String(64))
    dataProducerBy = db.Column(db.Integer)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            setattr(self, property, value)

    def __repr__(self):
        return str(self.producerApplicationName)

class kloudbeeBusinessGlossary(db.Model):

    __tablename__ = 'kloudbeeBusinessGlossary'

    id = db.Column(db.Integer, primary_key=True)
    businessGlossaryTerm = db.Column(db.String(255))
    businessDefinition = db.Column(db.String(1024))
    businessDomain = db.Column(db.String(255))
    termSource = db.Column(db.String(24))
    dataDomain = db.Column(db.String(255))
    businessSteward = db.Column(db.String(255))
    businessGlossaryOn = db.Column(db.String(64))
    businessGlossaryBy = db.Column(db.Integer)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            setattr(self, property, value)

    def __repr__(self):
        return str(self.businessGlossaryTerm)

class kloudbeeDataCatalogue(db.Model):

    __tablename__ = 'kloudbeeDataCatalogue'

    id = db.Column(db.Integer, primary_key=True)
    attributeName = db.Column(db.String(255))
    attributeDescription = db.Column(db.String(1024))
    tableName = db.Column(db.String(255))
    columnName = db.Column(db.String(255))
    columnDescription = db.Column(db.String(1024))
    columnDatatype = db.Column(db.String(32))
    isNullable = db.Column(db.Integer())
    isPrimaryKey = db.Column(db.Integer())
    isForeignKey = db.Column(db.Integer())
    attributeSensitivity = db.Column(db.String(255))
    termSource = db.Column(db.String(24))
    possibleValues = db.Column(db.String(255))
    valuesDescription = db.Column(db.String(1024))
    notes = db.Column(db.String(1024))
    catalogueAttributeCreatedOn = db.Column(db.String(64))
    catalogueAttributeCreatedBy = db.Column(db.Integer)
    catalogueAttributeUpdatedBy = db.Column(db.Integer)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            setattr(self, property, value)

    def __repr__(self):
        return str(self.attributeName)

class kloudbeeDataSets(db.Model):

    __tablename__ = 'kloudbeeDataSets'

    id = db.Column(db.Integer, primary_key=True)
    dataSetName = db.Column(db.String(255))
    dataSetDescription = db.Column(db.String(1024))
    dataSetCreatedOn = db.Column(db.String(64))
    dataSetCreatedBy = db.Column(db.Integer)
    dataSetUpdatedBy = db.Column(db.Integer)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            setattr(self, property, value)

    def __repr__(self):
        return str(self.dataSetName)

class kloudbeeDataSetFields(db.Model):

    __tablename__ = 'kloudbeeDataSetFields'

    id = db.Column(db.Integer, primary_key=True)
    dataSetId = db.Column(db.Integer)
    dataSetFieldName = db.Column(db.String(255))
    dataSetFieldValue = db.Column(db.String(255))
    dataSetCreatedOn = db.Column(db.String(64))
    dataSetCreatedBy = db.Column(db.Integer)
    dataSetUpdatedBy = db.Column(db.Integer)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            setattr(self, property, value)

    def __repr__(self):
        return str(self.dataSetFieldName)

class kloudbeeDataDomains(db.Model):

    __tablename__ = 'kloudbeeDataDomains'

    id = db.Column(db.Integer, primary_key=True)
    dataDomain = db.Column(db.String(255))
    dataDomainDescription = db.Column(db.String(1024))
    dataSetCreatedOn = db.Column(db.String(64))
    dataSetCreatedBy = db.Column(db.Integer)
    dataSetUpdatedBy = db.Column(db.Integer)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            setattr(self, property, value)

    def __repr__(self):
        return str(self.dataDomain)
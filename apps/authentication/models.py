# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present eSquare
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


class eSquareObservations(db.Model):

    __tablename__ = 'eSquareObservations'

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

class eSquareDataSources(db.Model):

    __tablename__ = 'eSquareDataSources'

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

class eSquareDataConsumers(db.Model):

    __tablename__ = 'eSquareDataConsumers'

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

class eSquareDataProducers(db.Model):

    __tablename__ = 'eSquareDataProducers'

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
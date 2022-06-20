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
    

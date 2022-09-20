# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present kloudbee
"""

from flask import Blueprint

blueprint = Blueprint(
    'authentication_blueprint',
    __name__,
    url_prefix=''
)

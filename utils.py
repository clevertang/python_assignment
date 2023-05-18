#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：python_assignment 
@File    ：utils.py
@Author  ：xin.tang
@Date    ：2023/5/16 20:56 
"""

import logging
import os
from functools import wraps
from logging.handlers import RotatingFileHandler

from flask import jsonify
from flask import request
from jsonschema import Draft4Validator, ValidationError


def configure_logging(file_name):
    log_dir = os.path.abspath('./log')
    if os.getenv('ENVIRONMENT'):
        log_dir = '/work/log'  # when local,local path depends on my file path
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, file_name)
    print(log_file)
    log_formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
    log_handler = RotatingFileHandler(log_file, maxBytes=1024 * 1024, backupCount=10)
    log_handler.setFormatter(log_formatter)

    _logger = logging.getLogger()  # add _ since i use logger outside
    _logger.addHandler(log_handler)
    _logger.setLevel(logging.INFO)

    return _logger


logger = configure_logging('request.log')


# Retry decorator
def retry_on_failure(max_retries=3):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logger.error(f"An error occurred: {str(e)}")
                    retries += 1
            raise Exception(f"Failed after {max_retries} retries")

        return wrapper

    return decorator


def normalize_data(schema, data):
    """
    if you do not use json to request ,every thing should be str,so we need this
    in this case i only deal with integer
    :return:
    """
    all_fields_detail = schema.get('properties')
    for filed_name, field_detail in all_fields_detail.items():
        if field_detail.get('type') == 'integer':
            if data.get(filed_name):
                try:
                    data[filed_name] = int(data[filed_name])
                except Exception as e:
                    raise Exception(
                        '{} can not covert to {},error msg is {}'.format(filed_name, field_detail.get('type'), str(e)))
    return data


def params_validator(schema):
    validator = Draft4Validator(schema)

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            formdata = request.args.copy()
            try:
                formdata = normalize_data(validator.schema, formdata)
                validator.validate(formdata)
                data = formdata
            except ValidationError as ex:
                # handle param validate error
                result = {
                    "data": [],
                    "pagination": {},
                    "info": {'error': ex.message}
                }

                return jsonify(result)
            except Exception as ex:
                # handle other exception
                result = {
                    "data": [],
                    "pagination": {},
                    "info": {'error': str(ex)}
                }
                return jsonify(result)
            return func(data, *args, **kwargs)

        return wrapper

    return decorator

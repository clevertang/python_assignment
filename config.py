#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：python_assignment
@File    ：config.py
@Author  ：xin.tang
@Date    ：2023/5/16 11:41
"""
import os

SYMBOLS = ["IBM", "AAPL"]
BASE_URL = "https://www.alphavantage.co/query"

DATABASE_URI = os.getenv(
    'DATABASE_URI', 'mysql://root:tx123321z@localhost/financial_data')  # use env to set some config
DATABASE_HOST = os.getenv('DATABASE_HOST', 'localhost')
DATABASE_NAME = 'financial_data'  # in this simple case,it's same
DATABASE_USER = 'root'
DATABASE_PASSWORD = 'tx123321z'





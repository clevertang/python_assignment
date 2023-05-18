#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：python_assignment 
@File    ：app.py
@Author  ：xin.tang
@Date    ：2023/5/16 12:18 
"""
import os
import sys

import pymysql
from apscheduler.triggers.cron import CronTrigger
from flask import Flask, jsonify

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(parent_dir)

from config import DATABASE_URI
from get_raw_data import get_raw_data
from model import db, FinancialData
from utils import params_validator, configure_logging
from apscheduler.schedulers.background import BackgroundScheduler

pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['DEBUG'] = True
db.init_app(app)
logger = configure_logging('app.log')
scheduler = BackgroundScheduler()
scheduler.start()
scheduler.add_job(get_raw_data, trigger=CronTrigger(day_of_week='*', hour='0', minute='0'))

PAGE_SCHEMA = {'type': 'integer', 'minimum': 1}

LIMIT_SCHEMA = {'type': 'integer', 'minimum': 1, 'maximum': 1000, 'description': 'maximum=1000'}

SIMPLE_DATE_PATTERN = '\d{4}-\d{2}-\d{2}'

DATE_SCHEMA = {'type': 'string', "pattern": SIMPLE_DATE_PATTERN}

GET_FINANCIAL_SCHEMA = {
    "type": "object",
    "properties": {
        "start_date": DATE_SCHEMA,
        "end_date": DATE_SCHEMA,
        "symbol": {'type': 'string'},  # no limit for me,but can add some re limit and all param are str
        "limit": LIMIT_SCHEMA,
        'page': PAGE_SCHEMA

    },
}


@app.route('/api/financial_data', methods=['GET'])
@params_validator(GET_FINANCIAL_SCHEMA)
def get_financial_data(data: dict) -> jsonify:
    # get params
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    symbol = data.get('symbol')
    limit = data.get('limit', 5)
    page = data.get('page', 1)

    # contract search filter
    query = FinancialData.query
    if start_date:
        query = query.filter(FinancialData.date >= start_date)
    if end_date:
        query = query.filter(FinancialData.date <= end_date)
    if symbol:
        query = query.filter(FinancialData.symbol == symbol)

    # page
    total_count = query.count()
    total_pages = (total_count + limit - 1) // limit
    offset = (page - 1) * limit
    data = query.order_by(FinancialData.date.desc()).offset(offset).limit(limit).all()

    # construct result
    result = {
        'data': [
            {
                'symbol': item.symbol,
                'date': item.date.strftime('%Y-%m-%d'),
                'open_price': str(item.open_price),
                'close_price': str(item.close_price),
                'volume': str(item.volume),
            }
            for item in data
        ],
        'pagination': {
            'count': total_count,
            'page': page,
            'limit': limit,
            'pages': total_pages,
        },
        'info': {'error': ''}
    }

    return jsonify(result)


GET_STATICS_SCHEMA = {
    "type": "object",
    "properties": {
        "start_date": DATE_SCHEMA,
        "end_date": DATE_SCHEMA,
        "symbol": {'type': 'string'}  # no limit for me,but can add some re limit and all param are str
    },
    "required": ["symbol", "start_date", "end_date"]
}


@app.route('/api/statistics', methods=['GET'])
@params_validator(GET_STATICS_SCHEMA)
def get_statistics(data: dict) -> jsonify:
    # get params
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    symbol = data.get('symbol')  # only one symbol

    # get filters and query
    query = FinancialData.query
    query = query.filter(FinancialData.date >= start_date) if start_date else query
    query = query.filter(FinancialData.date <= end_date) if end_date else query
    query = query.filter(FinancialData.symbol == symbol) if symbol else query

    # calculate statistics
    total_days = query.with_entities(FinancialData.date).distinct().count()
    total_volume = query.with_entities(db.func.sum(FinancialData.volume)).scalar()
    average_open_price = query.with_entities(db.func.avg(FinancialData.open_price)).scalar()
    average_close_price = query.with_entities(db.func.avg(FinancialData.close_price)).scalar()
    average_daily_volume = total_volume / total_days

    # construct result
    result = {
        'data': {
            'start_date': start_date,
            'end_date': end_date,
            'symbol': symbol,
            'average_daily_open_price': round(average_open_price, 2),
            # SELECT AVG(open_price) AS average_open_price
            # FROM financial_data
            # WHERE date >= (SELECT MAX(date) - INTERVAL 19 DAY FROM financial_data)
            # need to round it if use db to calculate
            # use db service of server service depends on different situation,mostly server is more scalable
            # this is just a simple case ,i choose use db
            'average_daily_close_price': round(average_close_price, 2),
            'average_daily_volume': int(average_daily_volume)
        },
        'info': {'error': ''}
    }
    return jsonify(result)


@app.route('/start_job', methods=['POST'])
def start_job() -> str:
    scheduler.print_jobs()  # print all task
    get_raw_data()  # action right now
    return 'task finished'


@app.errorhandler(Exception)
def handle_error(error: Exception) -> jsonify:
    response = {
        'data': [],
        'pagination': {},
        'info': {'error': str(error)}
    }
    return jsonify(response), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005)

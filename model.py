#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：python_assignment 
@File    ：models.py
@Author  ：xin.tang
@Date    ：2023/5/16 11:48 
"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class FinancialData(db.Model):
    __tablename__ = 'financial_data'
    id = db.Column(db.Integer, primary_key=True)  # better for btree storage
    symbol = db.Column(db.String(64))
    date = db.Column(db.Date)
    open_price = db.Column(db.Numeric(precision=12, scale=2))  #
    close_price = db.Column(db.Numeric(precision=12, scale=2))  #
    volume = db.Column(db.Numeric(precision=12, scale=0))  # as doc ,it's integer

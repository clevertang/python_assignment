#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：python_assignment 
@File    ：test_api.py
@Author  ：xin.tang
@Date    ：2023/5/18 10:57 
"""
import json
import pytest

from financial.app import app

# very simple case and you can also add it to build process


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_get_financial_data(client):
    response = client.get('/api/financial_data')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "data" in data
    assert "pagination" in data
    assert "info" in data


def test_get_statistics(client):
    response = client.get('/api/statistics')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "data" in data
    assert "info" in data

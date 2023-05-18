from datetime import datetime, timedelta

import pymysql
import requests
from config import SYMBOLS, BASE_URL, DATABASE_HOST, DATABASE_USER, DATABASE_PASSWORD, \
    DATABASE_NAME
from utils import configure_logging, retry_on_failure

logger = configure_logging('task.log')


def get_api_key():
    connection = pymysql.connect(host=DATABASE_HOST, user=DATABASE_USER, password=DATABASE_PASSWORD,
                                 database=DATABASE_NAME)
    cursor = connection.cursor()

    query = "SELECT value FROM config WHERE name='api_key'"
    cursor.execute(query)

    result = cursor.fetchone()
    cursor.close()
    connection.close()
    if result:
        return result[0]
    else:
        return None


API_KEY = get_api_key()


@retry_on_failure()
def get_data_from_source(symbol):
    """
    get data from source
    :param symbol:
    :return:
    """
    params = {
        "function": "TIME_SERIES_DAILY_ADJUSTED",  # daily function is not free
        "symbol": symbol,
        "apikey": API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code != 200:
        raise Exception('request {},{} failed'.format(BASE_URL, params))
    data = response.json()
    if "Time Series (Daily)" not in data:
        raise Exception('do not get data from source')
    return data


def get_raw_data():
    conn = pymysql.connect(host=DATABASE_HOST, user=DATABASE_USER, password=DATABASE_PASSWORD, database=DATABASE_NAME)
    cursor = conn.cursor()
    for symbol in SYMBOLS:
        # get data from the API
        data = get_data_from_source(symbol)
        daily_data = data["Time Series (Daily)"]
        today = datetime.now().date()
        two_weeks_ago = today - timedelta(days=13)  # 2 weeks
        for date, values in daily_data.items():
            # get date and data
            date_obj = datetime.strptime(date, "%Y-%m-%d").date()
            if not date_obj >= two_weeks_ago and date_obj <= today:  # i do not think it's necessary
                continue
            open_price = float(values["1. open"])
            close_price = float(values["4. close"])
            volume = int(values["6. volume"])
            # Use "INSERT INTO ... ON DUPLICATE KEY UPDATE" SQL statement, maybe we need to update the record
            sql = """
                    INSERT INTO financial_data (symbol, date, open_price, close_price, volume)
                    VALUES (%s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                    open_price = VALUES(open_price),
                    close_price = VALUES(close_price),
                    volume = VALUES(volume)
                    """
            values = (symbol, date_obj, open_price, close_price, volume)

            cursor.execute(sql, values)
    cursor.connection.commit()
    conn.close()


if __name__ == "__main__":
    logger.info('start request data from data source')
    get_raw_data()
    logger.info('finish request data from data source')

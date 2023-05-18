API Documentation

## Financial Data API

### Get Financial Data

Retrieves financial data based on specified filters.

**Endpoint:** `/api/financial_data`

**HTTP Method:** GET

**Parameters:**

- `start_date` (optional): The start date of the data range in the format 'YYYY-MM-DD'.
- `end_date` (optional): The end date of the data range in the format 'YYYY-MM-DD'.
- `symbol` (optional): The symbol of the financial data.
- `limit` (optional): The maximum number of results to return (default: 5).
- `page` (optional): The page number for pagination (default: 1).

**Response:**

- `data` (array): An array of financial data objects.
  - `symbol` (string): The symbol of the financial data.
  - `date` (string): The date of the financial data in the format 'YYYY-MM-DD'.
  - `open_price` (string): The opening price of the financial data.
  - `close_price` (string): The closing price of the financial data.
  - `volume` (string): The volume of the financial data.
- `pagination` (object): Pagination information.
  - `count` (integer): The total count of financial data records.
  - `page` (integer): The current page number.
  - `limit` (integer): The maximum number of results per page.
  - `pages` (integer): The total number of pages.
- `info` (object): Additional information.
  - `error` (string): Error message, if any.

**Example:**

Request:

```
GET /api/financial_data?start_date=2023-01-01&end_date=2023-01-10&symbol=IBM&limit=3&page=2
```

Response:

```json
{
  "data": [
    {
      "symbol": "IBM",
      "date": "2023-01-05",
      "open_price": "153.08",
      "close_price": "154.52",
      "volume": "62199013"
    },
    {
      "symbol": "IBM",
      "date": "2023-01-06",
      "open_price": "153.08",
      "close_price": "154.52",
      "volume": "59099013"
    },
    {
      "symbol": "IBM",
      "date": "2023-01-09",
      "open_price": "153.08",
      "close_price": "154.52",
      "volume": "42399013"
    }
  ],
  "pagination": {
    "count": 20,
    "page": 2,
    "limit": 3,
    "pages": 7
  },
  "info": {
    "error": ""
  }
}
```

## Statistics API

### Get Statistics

Calculates statistics based on specified filters.

**Endpoint:** `/api/statistics`

**HTTP Method:** GET

**Parameters:**

- `start_date` (required): The start date of the data range in the format 'YYYY-MM-DD'.
- `end_date` (required): The end date of the data range in the format 'YYYY-MM-DD'.
- `symbol` (optional): The symbol of the financial data.

**Response:**

- `data` (object): Statistics information.
  - `start_date` (string): The start date of the data range.
  - `end_date` (string): The end date of the data range.
  - `symbol` (string): The symbol of the financial data.
  - `average_daily_open
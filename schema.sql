CREATE TABLE IF NOT EXISTS financial_data (
    id INT NOT NULL AUTO_INCREMENT,
    symbol VARCHAR(255) NOT NULL,
    date DATE NOT NULL,
    open_price DECIMAL(12, 2) NOT NULL,
    close_price DECIMAL(12, 2) NOT NULL,
    volume INT NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY idx_unique_date_symbol (date, symbol)
);

CREATE TABLE config (
  id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(64),
  value VARCHAR(255)
);
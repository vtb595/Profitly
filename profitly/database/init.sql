CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(50) NOT NULL
);

CREATE TABLE portfolio (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    ticker VARCHAR(10),
    shares INTEGER
);

INSERT INTO users (username, password)
VALUES
('oliver', '123'),
('chris', '123'),
('ziad', '123'),
('seb', '123');

INSERT INTO portfolio (user_id, ticker, shares)
VALUES

-- Oliver
(1, 'AAPL', 5),
(1, 'MSFT', 2),
(1, 'NVDA', 1),

-- Chris
(2, 'TSLA', 3),
(2, 'AMZN', 1),
(2, 'META', 4),

-- Ziad
(3, 'GOOGL', 2),
(3, 'NFLX', 5),
(3, 'AMD', 10),

-- Seb
(4, 'PLTR', 8),
(4, 'COIN', 2),
(4, 'SMCI', 1);


# Profitly - Investment Portfolio Tracker

## Overview

Profitly is a simple investment portfolio tracking web application inspired by Nordnet.
The project was developed using Python, Flask, PostgreSQL, Docker, HTML/CSS, and JavaScript.

The purpose of the application is to allow users to:

* log in to their account
* view a stock portfolio
* see live stock prices
* track total portfolio value
* view a simple portfolio performance graph

The stock prices are fetched live using Yahoo Finance.

GitHub repository:

```bash
https://github.com/vtb595/Profitly.git
```

---

# Built With

The project uses the following technologies:

* Python
* Flask
* PostgreSQL
* Docker
* HTML
* CSS
* JavaScript
* Chart.js
* Yahoo Finance API (`yfinance`)
* Regex (`re`)

---

# Project Structure

```bash
PROFITLY/
│
├── app/
│   ├── static/
│   │   └── style.css
│   │
│   ├── templates/
│   │   ├── login.html
│   │   └── dashboard.html
│   │
│   ├── app.py
│   ├── db.py
│   └── requirements.txt
│
├── database/
│   └── init.sql
│
├── docker-compose.yml
├── Dockerfile
└── README.md
```

---

# Requirements

Before running the project, Docker Desktop must be installed.

Download Docker Desktop here:

```bash
https://www.docker.com/products/docker-desktop/
```

---

# Installation Instructions

## 1. Clone the repository

```bash
git clone https://github.com/vtb595/Profitly.git
```

---

## 2. Open the project folder

```bash
cd Profitly
```

Depending on how the project was downloaded, there may be **two project folders**.

For example, after opening the first folder, the project may contain another folder called `profitly` or `Profitly`.

To check this, run:

```bash
ls
```

If you see another project folder, open that folder as well. For example:

```bash
cd profitly
```

or, if the folder name uses a capital letter:

```bash
cd Profitly
```

The important thing is that you must be in the folder where `docker-compose.yml` is located.

You can check this by running:

```bash
ls
```

You should see something like:

```bash
docker-compose.yml
Dockerfile
app
database
requirements.txt
README.md
```

If you do not see `docker-compose.yml`, you are not in the correct folder yet.

---

## 3. Start Docker Desktop

Make sure Docker Desktop is running before continuing.

---

# Compilation / Execution Instructions

When you are in the folder containing `docker-compose.yml`, run:

```bash
docker compose up --build
```

If this command does not work, try the older Docker Compose command:

```bash
docker-compose up --build
```

This command will:

* build the Flask application
* create the PostgreSQL database
* initialize the SQL tables
* start the containers

If the terminal returns to the prompt immediately, or if the website does not open, try running the containers in detached mode:

```bash
docker compose up --build -d
```

You can check whether the containers are running with:

```bash
docker compose ps
```

You should see that the containers are marked as running.

If the application still does not work, you can restart everything with:

```bash
docker compose down
docker compose up --build
```

---

# Open the Application

When the containers are running, open the browser and go to:

```bash
http://localhost:5050
```

---

# Interaction Instructions

## Demo Users

The following users can log in:

| Username | Password |
| -------- | -------- |
| oliver   | 123      |
| chris    | 123      |
| ziad     | 123      |
| seb      | 123      |

---

# Features

## Login System

The application includes:

* user login
* SQL authentication
* regex username validation

Regex example:

```python
username_pattern = r"^[a-zA-Z0-9_]+$"
```

This ensures usernames only contain:

* letters
* numbers
* underscores

---

## Portfolio Dashboard

After login, the user can:

* view owned stocks
* view live stock prices
* view number of shares
* view total portfolio value
* view portfolio graph
* view watchlist
* view market news

---

# Database

The project uses PostgreSQL.

The database contains two tables:

## users

Stores usernames and passwords.

## portfolio

Stores:

* stock ticker
* shares
* user id

Example SQL query:

```python
cur.execute(
    "SELECT ticker, shares FROM portfolio WHERE user_id=%s",
    (user_id,)
)
```

---

# APIs Used

The application uses Yahoo Finance through the Python package `yfinance`.

Example:

```python
yf_stock = yf.Ticker(ticker)
price = yf_stock.info.get("currentPrice", 0)
```

---

# Stopping the Application

To stop the application:

```bash
CTRL + C
```

To stop Docker completely:

```bash
docker compose down
```

If your Docker setup uses the older command, use:

```bash
docker-compose down
```

---

# Authors

* Oliver lfq502
* Chris vtb595
* Ziad qpd834
* Seb xmz167

---

# Notes

This project was created as a student project and prototype.

The stock prices depend on Yahoo Finance and may vary depending on market opening hours.

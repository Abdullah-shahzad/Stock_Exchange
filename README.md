# Stock Exchange API

This project is a simple **Stock Exchange API** built using Django and Django REST Framework. It allows users to create accounts, add stocks, and manage stock transactions (buying and selling).

## Features

- **User Management**: Create and retrieve users.
- **Stock Management**: Add new stocks and list available stocks.
- **Transaction Management**: Perform stock transactions (buy/sell) with balance validation.
- **Transaction History**: Retrieve transaction history by user and filter by timestamp.

## Tech Stack

- **Django**: 5.1.1
- **Django REST Framework**: 3.15.2
- **PostgreSQL**: via psycopg2
- **drf-yasg**: 1.21.7 for API documentation

## Requirements

- Python 3.x
- PostgreSQL
- pip

## Installation

1. Clone the repository:
   ```bash
   [git clone https://github.com/your-repository-link.git](https://github.com/Abdullah-shahzad/Stock_Exchange)

2. Navigate into the project directory: 
   
    cd stock_exchange_project

3. Install the required dependencies: 
     pip install -r requirements.txt
   
5. Set up the PostgreSQL database and configure the connection in settings.py.

6. Run migrations to set up the database schema: 

   python manage.py migrate
  
7. Start the development server:
   python manage.py runserver

   
## API Endpoints

| Endpoint                                      | Method | Description                                       |
|-----------------------------------------------|--------|---------------------------------------------------|
| `/users/`                                     | POST   | Create a new user.                                |
| `/users/<str:username>/`                      | GET    | Retrieve user details by username.                |
| `/create_stock/`                              | POST   | Create a new stock.                               |
| `/stocks/`                                    | GET    | List all available stocks.                        |
| `/stocks/<str:ticker>/`                       | GET    | Retrieve stock data by ticker.                    |
| `/transactions/`                              | POST   | Create a new transaction (Buy/Sell stock).        |
| `/transactions/<str:username>/`               | GET    | List all transactions for a specific user.        |
| `/transactions/<str:username>/<str:start_time>/<str:end_time>/` | GET | List transactions by user within a time range.    |


#Models
User
* username: The username of the user (unique).
* balance: The balance available for transactions.
Stocks
* ticker: Stock ticker symbol (unique).
* stock_price: The price of the stock.
* stock_name: The name of the stock.
Transaction
* user: The user associated with the transaction.
* ticker: The stock involved in the transaction.
* transaction_type: Either 'BUY' or 'SELL'.
* transaction_volume: The amount of stock bought or sold.
* transaction_price: The price of the transaction.
* created_time: The time when the transaction was created. 
API Documentation
This project uses drf-yasg to generate and display interactive API documentation. You can view it at:
http://127.0.0.1:8000/swagger/

Contact
If you have any questions, feel free to contact me at abdullahkpr22@gmail.com





## GIVEN TASK:
Endpoints
POST /users/: To register a new user with a username and initial balance.
GET /users/{username}/: To retrieve user data. 
POST /stocks/: To ingest stock data and store it in the Postgres database.
GET /stocks/: To retrieve all stock data.
GET /stocks/{ticker}/: To retrieve specific stock data.
POST /transactions/: To post a new transaction. This should take user_id, ticker, transaction_type, and transaction_volume as inputs. The endpoint should calculate the transaction_price based on the current stock price and update the user's balance.
GET /transactions/{user_id}/: To retrieve all transactions of a specific user.
GET /transactions/{user_id}/{start_timestamp}/{end_timestamp}/: To retrieve transactions of a specific user between two timestamps.
Instruction
Add Swagger documentation.
The processing should validate the transaction (e.g., check if the user has enough balance for a buy transaction) and update the Users and Transactions tables accordingly.
Note:
Send a PR for the rest app.
Add the README.md file so that I can set up the project on my machine and can run it by following the README.md
Also, follow the standards for writing the rest app.


## pending
authentication
swagger(required field implementation)


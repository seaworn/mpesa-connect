# DARAJA CONNECT

A wrapper library for the Daraja Mpesa API

[![Language](https://img.shields.io/badge/language-python-green.svg)](https://python.org)

## Features

- Authorization
- Mpesa Express
  - STK Push
  - Query
- Customer To Business (C2B)
    - Register URL
    - Simulate
- Business To Customer (B2C)
- Account Balance
- Transaction Status

## Installation

    $ pip install daraja-connect

## Usage

*NOTE: Before you start, make sure to go through the official Daraja Mpesa API [documentation](https://developer.safaricom.co.ke/Documentation)* 

Create an app instance. 

```python
from daraja_connect import App

# Sandbox
app = App.create_sandbox(consumer_key=..., consumer_secret=...)

# Production
app = App.create_production(consumer_key=..., consumer_secret=...)
```

Generate an authorization token.

```python
from daraja_connect import Authorization

auth = Authorization(app)
result = auth.generate_token()
access_token = result.access_token
```
*You can attach this token to the service instance or include it as an argument to the api methods calls*

### Mpesa Express

**STK Push**
```python
from daraja_connect import STKPush

stk = STKPush(app, access_token=access_token)
result = stk.process_request(
    business_short_code=...,
    phone_number=...,
    amount=...,
    call_back_url=...,
    account_reference=...,
    transaction_desc=...,
    password=...,
    timestamp=...,
)
```

**Query**
```python
result = stk.query(
    business_short_code=...,
    checkout_request_id=...,
    password=...,
)
```
You can use the `generate_password` helper to create a password

```python
from daraja_connect.utils import generate_password

password = generate_password(
    business_short_code=....,
    pass_key=...,
    timestamp=...,
)
```
Alternatively, you can include the `pass_key` argument in place of `password` to auto generate the password

### Customer To Business (C2B) API

**Register URL**
```python
from daraja_connect import C2B
from daraja_connect.enums import ResponseType

c2b = C2B(app, access_token=access_token)
result = c2b.register_url(
    short_code=...,
    validation_url=...,
    confirmation_url=...,
    response_type=ResponseType.COMPLETED,
)
```

**Simulate**
```python
result = c2b.simulate(
    short_code=...,
    command_id=TransactionType.CUSTOMER_PAY_BILL_ONLINE,
    amount=...,
    msisdn=...,
    bill_ref_number=...,
)
```

### Business To Customer (B2C) API

```python
from daraja_connect import B2C
from daraja_connect.enums import TransactionType

b2c = B2C(app, access_token=access_token)
result = b2c.payment_request(
    initiator_name=...,
    security_credential=...,
    amount=...,
    command_id=TransactionType.BUSINESS_PAYMENT,
    party_a=...,
    party_b=...,
    queue_time_out_url=...,
    result_url=...,
    remarks=...,
    occassion=...,
)
```

### Account Balance API

```python
from daraja_connect import AccountBalance
from daraja_connect.enums import TransactionType, IdentifierType

ab = AccountBalance(app, access_token=access_token)
result = ab.query(
    initiator=...,
    security_credential=...,
    command_id=TransactionType.ACCOUNT_BALANCE,
    identifier_type=IdentifierType.ORGANIZATION_SHORT_CODE,
    party_a=...,
    queue_time_out_url=...,
    result_url=...,
    remarks=...,
)
```

### Transaction Status API

```python
from daraja_connect import TransactionStatus
from daraja_connect.enums import TransactionType, IdentifierType

ts = TransactionStatus(app, access_token=access_token)
result = ts.query(
    initiator=...,
    security_credential=...,
    transaction_id=...,
    command_id=TransactionType.TRANSACTION_STATUS_QUERY,
    identifier_type=IdentifierType.ORGANIZATION_SHORT_CODE,
    party_a=...,
    queue_time_out_url=...,
    result_url=...,
    remarks=...,
    occassion=...,
)
```

All API methods return a result object with a response property which is a [`requests.Response`](https://requests.readthedocs.io/en/latest/api/#requests.Response) object and various properties corresponding to the json body of the response

## Running Tests

Install dependencies

    $ poetry install

Create `.env` file from [.env.example](https://github.com/enwawerueli/daraja-connect/blob/main/.env.example) then edit it to add your app credentials and test parameters

    $ cp .env.example .env

 Run tests

    $ poetry run pytest

## License

[MIT](https://github.com/enwawerueli/daraja-connect/blob/main/LICENSE)

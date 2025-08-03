# MPESA CONNECT

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

    $ pip install mpesa-connect

## Usage

*NOTE: Before you start, make sure to go through the official Daraja Mpesa API [documentation](https://developer.safaricom.co.ke/Documentation)* 

Create an app instance. 

```python
from mpesa_connect import App, AppEnv

app = App(env=AppEnv.SANDBOX, consumer_key=..., consumer_secret=...)
```

### Authorization

Generate an authorization token.

```python
from mpesa_connect import OAuth

oauth = OAuth(app)
result = oauth.generate()
if result.status_ok:
    access_token = result.access_token
```
*You can attach this token to the api instance or include it as an argument to the api method call*

### Mpesa Express

#### STK Push
```python
from mpesa_connect import STKPush, TransactionType

stkpush = STKPush(app, access_token="your access token")
result = stkpush.process_request(
    business_short_code=...,
    phone_number=...,
    amount=...,
    call_back_url=...,
    account_reference=...,
    transaction_desc=...,
    transaction_type=TransactionType.CUSTOMER_PAY_BILL_ONLINE
    password=...,
    timestamp=...,
)
```

#### STK Push Query
```python
result = stkpush.query(
    business_short_code=...,
    checkout_request_id=...,
    password=...,
)
```
You can use the `generate_password` helper to create a password

```python
from mpesa_connect.utils import generate_password

password = generate_password(
    business_short_code=....,
    pass_key=...,
    timestamp=...,
)
```
Alternatively, you can include the `pass_key` argument in place of `password` to auto generate the password

### Customer To Business (C2B)

#### Register URL
```python
from mpesa_connect import C2B, CommandID, ResponseType, TransactionType

c2b = C2B(app, access_token="your access token")
result = c2b.register_url(
    short_code=...,
    validation_url=...,
    confirmation_url=...,
    response_type=ResponseType.COMPLETED,
)
```

### Business To Customer (B2C)

```python
from mpesa_connect import B2C, CommandID

b2c = B2C(app, access_token="your access token")
result = b2c.payment_request(
    originator_conversation_id=...,
    initiator_name=...,
    security_credential=...,
    amount=...,
    command_id=CommandID.BUSINESS_PAYMENT,
    party_a=...,
    party_b=...,
    queue_time_out_url=...,
    result_url=...,
    remarks=...,
    occassion=...,
)
```

### Account Balance

```python
from mpesa_connect import AccountBalance, CommandID, IdentifierType

bal = AccountBalance(app, access_token="your access token")
result = bal.query(
    initiator=...,
    security_credential=...,
    command_id=CommandID.ACCOUNT_BALANCE,
    identifier_type=IdentifierType.ORGANIZATION_SHORT_CODE,
    party_a=...,
    queue_time_out_url=...,
    result_url=...,
    remarks=...,
)
```

### Transaction Status

```python
from mpesa_connect import TransactionStatus, CommandID, IdentifierType

status = TransactionStatus(app, access_token="your access token")
result = status.query(
    initiator=...,
    security_credential=...,
    transaction_id=...,
    command_id=CommandID.TRANSACTION_STATUS_QUERY,
    identifier_type=IdentifierType.ORGANIZATION_SHORT_CODE,
    party_a=...,
    queue_time_out_url=...,
    result_url=...,
    remarks=...,
    occassion=...,
)
```

All API methods return either a `*Result` or `*ErrorResult` object based on whether the request was successful or not.

The result object has a `response` property which is a [`requests.Response`](https://requests.readthedocs.io/en/latest/api/#requests.Response) object, plus various other properties corresponding to the json body of the response. 

The result also has a `status_ok` property which you can use to discriminate between success and error results.

## Running Tests

Install dependencies

    $ poetry install

 Run tests

    $ poetry run pytest

## License

[MIT](https://github.com/enwawerueli/mpesa-connect/blob/main/LICENSE)

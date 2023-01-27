import pytest
from typing import cast
from dotenv import dotenv_values

from daraja_connect import (
    App,
    Authorization,
    STKPush,
    C2B,
    B2C,
    AccountBalance,
    TransactionStatus,
)
from daraja_connect.enums import ResponseType, TransactionType, IdentifierType

env = dotenv_values()


@pytest.fixture(scope="module")
def app() -> App:
    return App.create_sandbox(
        consumer_key=env["CONSUMER_KEY"],
        consumer_secret=env["CONSUMER_SECRET"],
    )


@pytest.fixture
def access_token(app: App) -> str:
    return cast(str, Authorization(app).generate_token().access_token)


def test_authorization(app: App) -> None:
    auth = Authorization(app)
    result = auth.generate_token()
    assert result.response.status_code == 200 and result.access_token


def test_stkpush_process_request(app: App, access_token: str) -> None:
    stk = STKPush(app, access_token=access_token)
    result = stk.process_request(
        business_short_code=cast(int, env["STKPUSH_BUSINESS_SHORT_CODE"]),
        phone_number=cast(int, env["STKPUSH_PHONE_NUMBER"]),
        amount=1,
        call_back_url=cast(str, env["STKPUSH_CALLBACK_URL"]),
        account_reference="ABC",
        transaction_desc="Pay KSH1 to ABC",
        pass_key=env["PASS_KEY"],
    )
    # print(result)
    assert result.response.status_code == 200 and result.response_code == "0"


def test_stkpush_query(app: App, access_token: str) -> None:
    stk = STKPush(app, access_token=access_token)
    result = stk.query(
        business_short_code=cast(int, env["STKPUSH_BUSINESS_SHORT_CODE"]),
        checkout_request_id=cast(str, env["STKPUSHQUERY_CHECKOUT_REQUEST_ID"]),
        pass_key=env["PASS_KEY"],
    )
    # print(result)
    assert result.response.status_code == 200 and result.response_code == "0"


def test_c2b_register_url(app: App, access_token: str) -> None:
    short_code = cast(int, env["C2B_SHORT_CODE"])
    c2b = C2B(app, access_token=access_token)
    result = c2b.register_url(
        short_code=short_code,
        validation_url=cast(str, env["C2B_VALIDATION_URL"]),
        confirmation_url=cast(str, env["C2B_CONFIRMATION_URL"]),
        response_type=ResponseType.COMPLETED,
    )
    # print(result)
    assert result.response.status_code == 200 and result.response_code == "0"


def test_c2b_simulate(app: App, access_token: str) -> None:
    c2b = C2B(app, access_token=access_token)
    result = c2b.simulate(
        short_code=cast(int, env["C2B_SHORT_CODE"]),
        command_id=TransactionType.CUSTOMER_PAY_BILL_ONLINE,
        amount=1,
        msisdn=cast(int, env["C2B_PHONE_NUMBER"]),
        bill_ref_number="BL/001",
    )
    # print(result)
    assert result.response.status_code == 200 and result.response_code == "0"


def test_b2c_payment_request(app: App, access_token: str) -> None:
    b2c = B2C(app, access_token=access_token)
    result = b2c.payment_request(
        initiator_name=cast(str, env["B2C_INITIATOR_NAME"]),
        security_credential=cast(str, env["B2C_SECURITY_CREDENTIAL"]),
        amount=1,
        command_id=TransactionType.BUSINESS_PAYMENT,
        party_a=cast(int, env["B2C_PARTY_A"]),
        party_b=cast(int, env["B2C_PARTY_B"]),
        queue_time_out_url=cast(str, env["B2C_QUEUE_TIMEOUT_URL"]),
        result_url=cast(str, env["B2C_RESULT_URL"]),
        remarks="Business payment",
        occassion="",
    )
    # print(result)
    assert result.response.status_code == 200 and result.response_code == "0"


def test_account_balance_query(app: App, access_token: str) -> None:
    ab = AccountBalance(app, access_token=access_token)
    result = ab.query(
        initiator=cast(str, env["ACCOUNT_BALANCE_INITIATOR"]),
        security_credential=cast(str, env["ACCOUNT_BALANCE_SECURITY_CREDENTIAL"]),
        identifier_type=IdentifierType.ORGANIZATION_SHORT_CODE,
        command_id=TransactionType.ACCOUNT_BALANCE,
        party_a=cast(int, env["ACCOUNT_BALANCE_PARTY_A"]),
        queue_time_out_url=cast(str, env["ACCOUNT_BALANCE_QUEUE_TIMEOUT_URL"]),
        result_url=cast(str, env["ACCOUNT_BALANCE_RESULT_URL"]),
        remarks="Account balance",
    )
    # print(result)
    assert result.response.status_code == 200 and result.response_code == "0"


def test_transaction_status_query(app: App, access_token: str) -> None:
    ts = TransactionStatus(app, access_token=access_token)
    result = ts.query(
        initiator=cast(str, env["TRANSACTION_STATUS_INITIATOR"]),
        security_credential=cast(str, env["TRANSACTION_STATUS_SECURITY_CREDENTIAL"]),
        transaction_id=cast(str, env["TRANSACTION_STATUS_TRANSACTION_ID"]),
        identifier_type=IdentifierType.ORGANIZATION_SHORT_CODE,
        command_id=TransactionType.TRANSACTION_STATUS_QUERY,
        party_a=cast(int, env["TRANSACTION_STATUS_PARTY_A"]),
        queue_time_out_url=cast(str, env["TRANSACTION_STATUS_QUEUE_TIMEOUT_URL"]),
        result_url=cast(str, env["TRANSACTION_STATUS_RESULT_URL"]),
        remarks="Transaction status",
        occassion="",
    )
    # print(result)
    assert result.response.status_code == 200 and result.response_code == "0"

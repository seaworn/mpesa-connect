import pytest
import responses

from mpesa_connect import (
    B2C,
    C2B,
    AccountBalance,
    AccountBalanceResult,
    App,
    AppEnv,
    B2CResult,
    C2BResult,
    CommandID,
    IdentifierType,
    OAuth,
    OAuthResult,
    QRCode,
    QRCodeResult,
    ResponseType,
    STKPush,
    STKPushQueryResult,
    STKPushResult,
    TransactionStatus,
    TransactionStatusResult,
    TransactionType,
    TrxCode,
)

SANDBOX_URL = "https://sandbox.safaricom.co.ke"
LIVE_URL = "https://api.safaricom.co.ke"


@pytest.fixture(scope="module")
def app() -> App:
    return App(env=AppEnv.SANDBOX, consumer_key="", consumer_secret="")


def test_app_env():
    kw = {"consumer_key": "", "consumer_secret": ""}
    s0 = App(env=AppEnv.SANDBOX, **kw)
    s1 = App(env="sandbox", **kw)
    s2 = App.create_sandbox(**kw)
    l0 = App(env=AppEnv.LIVE, **kw)
    l1 = App(env="live", **kw)
    l2 = App.create_live(**kw)
    assert s0.base_url == s1.base_url == s2.base_url == SANDBOX_URL
    assert l0.base_url == l1.base_url == l2.base_url == LIVE_URL


@responses.activate
def test_authorization(app: App) -> None:
    responses.get(
        f"{SANDBOX_URL}/oauth/v1/generate",
        json={"access_token": "c9SQxWWhmdVRlyh0zh8gZDTkubVF", "expires_in": "3599"},
        status=200,
    )
    auth = OAuth(app)
    result = auth.generate()
    assert result.response.status_code == 200
    assert result == OAuthResult(
        response=result.response,
        status_ok=True,
        access_token="c9SQxWWhmdVRlyh0zh8gZDTkubVF",
        expires_in="3599",
    )


@responses.activate
def test_stkpush_process_request(app: App) -> None:
    responses.post(
        f"{SANDBOX_URL}/mpesa/stkpush/v1/processrequest",
        json={
            "MerchantRequestID": "29115-34620561-1",
            "CheckoutRequestID": "ws_CO_191220191020363925",
            "ResponseCode": "0",
            "ResponseDescription": "Success. Request accepted for processing",
            "CustomerMessage": "Success. Request accepted for processing",
        },
        status=200,
    )

    result = STKPush(app).process_request(
        business_short_code="174379",
        phone_number="254708374149",
        amount="1",
        call_back_url="https://mydomain.com/pat",
        account_reference="Test",
        transaction_desc="Test",
        transaction_type=TransactionType.CUSTOMER_PAY_BILL_ONLINE,
        password="MTc0Mzc5YmZiMjc5ZjlhYTliZGJjZjE1OGU5N2RkNzFhNDY3Y2QyZTBjODkzMDU5YjEwZjc4ZTZiNzJhZGExZWQyYzkxOTIwMTYwMjE2MTY1NjI3",
        timestamp="20160216165627",
    )
    assert result.response.status_code == 200
    assert result == STKPushResult(
        response=result.response,
        status_ok=True,
        merchant_request_id="29115-34620561-1",
        checkout_request_id="ws_CO_191220191020363925",
        response_code="0",
        response_description="Success. Request accepted for processing",
        customer_message="Success. Request accepted for processing",
    )


@responses.activate
def test_stkpush_query(app: App) -> None:
    responses.post(
        f"{SANDBOX_URL}/mpesa/stkpushquery/v1/query",
        json={
            "ResponseCode": "0",
            "ResponseDescription": "The service request has been accepted successfully",
            "MerchantRequestID": "22205-34066-1",
            "CheckoutRequestID": "ws_CO_13012021093521236557",
            "ResultCode": "0",
            "ResultDesc": "The service request is processed successfully.",
        },
        status=200,
    )
    result = STKPush(app).query(
        business_short_code="174379",
        checkout_request_id="ws_CO_13012021093521236557",
        password="MTc0Mzc5YmZiMjc5TliZGJjZjE1OGU5N2RkNzFhNDY3Y2QyZTBjODkzMDU5YjEwZjc4ZTZiNzJhZGExZWQyYzkxOTIwMTYwMjE2MTY1NjI3",
        timestamp="20160216165627",
    )
    assert result.response.status_code == 200
    assert result == STKPushQueryResult(
        response=result.response,
        status_ok=True,
        response_code="0",
        response_description="The service request has been accepted successfully",
        merchant_request_id="22205-34066-1",
        checkout_request_id="ws_CO_13012021093521236557",
        result_code="0",
        result_desc="The service request is processed successfully.",
    )


@responses.activate
def test_c2b_register_url(app: App) -> None:
    responses.post(
        f"{SANDBOX_URL}/mpesa/c2b/v1/registerurl",
        json={
            "OriginatorConversationID": "df2b-4546-bd46-7ed17f22e0b542692",
            "ResponseCode": "0",
            "ResponseDescription": "Success",
        },
        status=200,
    )
    result = C2B(app).register_url(
        short_code="600983",
        response_type=ResponseType.COMPLETED,
        validation_url="https://mydomain.com/validation",
        confirmation_url="https://mydomain.com/confirmation",
    )
    assert result.response.status_code == 200
    assert result == C2BResult(
        response=result.response,
        status_ok=True,
        originator_conversation_id="df2b-4546-bd46-7ed17f22e0b542692",
        response_code="0",
        response_description="Success",
    )


@responses.activate
def test_b2c_payment_request(app: App) -> None:
    responses.post(
        f"{SANDBOX_URL}/mpesa/b2c/v1/paymentrequest",
        json={
            "ConversationID": "AG_20250803_0100100304l06pxff5wk",
            "OriginatorConversationID": "2dc26700-cdce-41a8-9913-d8a35704cd48",
            "ResponseCode": "0",
            "ResponseDescription": "Accept the service request successfully.",
        },
        status=200,
    )
    result = B2C(app).payment_request(
        originator_conversation_id="2dc26700-cdce-41a8-9913-d8a35704cd48",
        initiator_name="testapi",
        security_credential="XqNCoHU62L1BscmGuzO2cC0SbFHUaqzzBiPi0p2bUxfFNajFv6Q2pjQ43tUTimLHjSAg+D/Eyfmz3xASFemb4kV6/WkGWldCsajxFSZpKNLSsFhdkSHx41jcLzdxM14JthcSfWes4GBnDZrnhUMt/wNIScBwar+tLKBORIGXV9Vf5BfDKtXo7fyciLfe89TfcCacMHMoO9Ox9XVoFbCZ9S0BFjiG3BaDqBL98yCyc6bVCGych7sewGInSdonM8ZG9V5Qii3gduUVy5/+4070fAkvMecvfCwsORlLe4ZTpM1cRnGiKebR/+SvzYkH1avsBJJ+NcEx0sTxf6AnL+JIgg==",
        command_id=CommandID.BUSINESS_PAYMENT,
        amount="1",
        party_a="600979",
        party_b="254708374149",
        remarks="Test remarks",
        queue_time_out_url="https://mydomain.com/b2c/queue",
        result_url="https://mydomain.com/b2c/result",
        occassion="null",
    )
    assert result.response.status_code == 200
    assert result == B2CResult(
        response=result.response,
        status_ok=True,
        conversation_id="AG_20250803_0100100304l06pxff5wk",
        originator_conversation_id="2dc26700-cdce-41a8-9913-d8a35704cd48",
        response_code="0",
        response_description="Accept the service request successfully.",
    )


@responses.activate
def test_account_balance_query(app: App) -> None:
    responses.post(
        f"{SANDBOX_URL}/mpesa/accountbalance/v1/query",
        json={
            "OriginatorConversationID": "c9aa-485e-a88a-be3f936aa2bc42901",
            "ConversationID": "AG_20250803_0100200305b1x5r6deab",
            "ResponseCode": "0",
            "ResponseDescription": "Accept the service request successfully.",
        },
        status=200,
    )
    result = AccountBalance(app).query(
        initiator="testapi",
        security_credential="Jh0085FKhus6kroi4/dl14APsGAZx9ioH9B1oV3TG3ZTmn1k7CxvIdzNbx8fVFmRlNQwugH3RK7JiRzks96hMKKjQSkj7N8qehDaGqyK+sP6GCZVm13HUYC5OXNK1jOG3VC4v9qlpGmVkhgdcadD3J5ix8khrxzC+TVRM6XMcZjvecLtEmJ3DDXQq2okGZW2uc/bHYEZTThmo5lNA+hpI/ZTMylnYsALal22w0WwIC3bjmvFDC+eHv08FJ1foJ5DCtYsRt8P2cweB9qZ8qVMlDI+mce/n8+SOUWKEosV00WxFO8X4cfHnGmy6woVLCLloTvhEOv0sz1EP8XQ/JvH0g==",
        command_id=CommandID.ACCOUNT_BALANCE,
        identifier_type=IdentifierType.TILL_NUMBER,
        party_a="600987",
        remarks="Test Remarks",
        queue_time_out_url="https://mydomain.com/AccountBalance/queue/",
        result_url="https://mydomain.com/AccountBalance/result/",
    )
    assert result.response.status_code == 200
    assert result == AccountBalanceResult(
        response=result.response,
        status_ok=True,
        originator_conversation_id="c9aa-485e-a88a-be3f936aa2bc42901",
        conversation_id="AG_20250803_0100200305b1x5r6deab",
        response_code="0",
        response_description="Accept the service request successfully.",
    )


@responses.activate
def test_transaction_status_query(app: App) -> None:
    responses.post(
        f"{SANDBOX_URL}/mpesa/transactionstatus/v1/query",
        json={
            "ConversationID": "AG_20250803_0100100304l06pxff5wk",
            "OriginatorConversationID": "2dc26700-cdce-41a8-9913-d8a35704cd48",
            "ResponseCode": "0",
            "ResponseDescription": "Accept the service request successfully.",
        },
        status=200,
    )
    result = TransactionStatus(app).query(
        initiator="testapi",
        security_credential="Jh0085FKhus6kroi4/dl14APsGAZx9ioH9B1oV3TG3ZTmn1k7CxvIdzNbx8fVFmRlNQwugH3RK7JiRzks96hMKKjQSkj7N8qehDaGqyK+sP6GCZVm13HUYC5OXNK1jOG3VC4v9qlpGmVkhgdcadD3J5ix8khrxzC+TVRM6XMcZjvecLtEmJ3DDXQq2okGZW2uc/bHYEZTThmo5lNA+hpI/ZTMylnYsALal22w0WwIC3bjmvFDC+eHv08FJ1foJ5DCtYsRt8P2cweB9qZ8qVMlDI+mce/n8+SOUWKEosV00WxFO8X4cfHnGmy6woVLCLloTvhEOv0sz1EP8XQ/JvH0g==",
        command_id=CommandID.TRANSACTION_STATUS_QUERY,
        transaction_id="NEF61H8J60",
        originator_conversation_id="AG_20190826_0000777ab7d848b9e721",
        party_a="600782",
        identifier_type=IdentifierType.ORGANIZATION_SHORT_CODE,
        result_url="https://mydomain.com/AccountBalance/result/",
        queue_time_out_url="https://mydomain.com/AccountBalance/queue/",
        remarks="Test Remarks",
        occassion="null",
    )
    assert result.response.status_code == 200
    assert result == TransactionStatusResult(
        response=result.response,
        status_ok=True,
        conversation_id="AG_20250803_0100100304l06pxff5wk",
        originator_conversation_id="2dc26700-cdce-41a8-9913-d8a35704cd48",
        response_code="0",
        response_description="Accept the service request successfully.",
    )


@responses.activate
def test_qrcode_generate(app: App) -> None:
    responses.post(
        f"{SANDBOX_URL}/mpesa/qrcode/v1/generate",
        json={
            "ResponseCode": "00",
            "ResponseDescription": "QR Code Successfully Generated.",
            "QRCode": "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",
        },
        status=200,
    )
    result = QRCode(app).generate(
        merchant_name="Test",
        ref_no="Test",
        amount="1",
        trx_code=TrxCode.BG,
        cpi="373132",
        size="300",
    )
    assert result.response.status_code == 200
    assert result == QRCodeResult(
        response=result.response,
        status_ok=True,
        response_code="00",
        response_description="QR Code Successfully Generated.",
        qr_code="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",
    )

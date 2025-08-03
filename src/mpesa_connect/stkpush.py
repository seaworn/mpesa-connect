from dataclasses import dataclass
from typing import Optional, Tuple, Union

import requests

from .base import API, ErrorResult, Result
from .enums import TransactionType
from .urls import PATH_STKPUSH_PROCESSREQUEST, PATH_STKPUSHQUERY_QUERY
from .utils import generate_password, str_now


@dataclass
class STKPushResult(Result):
    response_code: str
    response_description: str
    customer_message: str
    checkout_request_id: str
    merchant_request_id: str


@dataclass
class STKPushErrorResult(ErrorResult):
    pass


@dataclass
class STKPushQueryResult(Result):
    response_code: str
    response_description: str
    merchant_request_id: str
    checkout_request_id: str
    result_code: str
    result_desc: str


@dataclass
class STKPushQueryErrorResult(ErrorResult):
    pass


class STKPush(API):
    def process_request(
        self,
        *,
        business_short_code: Union[str, int],
        amount: Union[str, int],
        phone_number: Union[str, int],
        call_back_url: str,
        account_reference: str,
        transaction_desc: str,
        transaction_type: Union[TransactionType, str],
        party_a: Optional[str] = None,
        party_b: Optional[str] = None,
        password: Optional[str] = None,
        timestamp: Optional[str] = None,
        pass_key: Optional[str] = None,
        access_token: Optional[str] = None,
    ) -> Union[STKPushResult, STKPushErrorResult]:
        if not password:
            password, timestamp = self._generate_password(
                business_short_code,
                pass_key,
                timestamp,
            )
        payload = {
            "BusinessShortCode": business_short_code,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": (
                transaction_type.value
                if isinstance(transaction_type, TransactionType)
                else transaction_type
            ),
            "Amount": amount,
            "PartyA": party_a or phone_number,
            "PartyB": party_b or business_short_code,
            "PhoneNumber": phone_number,
            "CallBackURL": call_back_url,
            "AccountReference": account_reference,
            "TransactionDesc": transaction_desc,
        }
        response = requests.post(
            self.get_url(PATH_STKPUSH_PROCESSREQUEST),
            headers={"Authorization": f"Bearer {access_token or self.access_token}"},
            json=payload,
        )
        result_dict = self._make_result(response)
        if response.status_code != 200:
            return STKPushErrorResult(**result_dict)
        return STKPushResult(**result_dict)

    def query(
        self,
        *,
        business_short_code: Union[str, int],
        checkout_request_id: str,
        password: Optional[str] = None,
        timestamp: Optional[str] = None,
        pass_key: Optional[str] = None,
        access_token: Optional[str] = None,
    ) -> Union[STKPushQueryResult, STKPushQueryErrorResult]:
        if not password:
            password, timestamp = self._generate_password(
                business_short_code,
                pass_key,
                timestamp,
            )
        payload = {
            "BusinessShortCode": business_short_code,
            "Password": password,
            "Timestamp": timestamp,
            "CheckoutRequestID": checkout_request_id,
        }
        response = requests.post(
            self.get_url(PATH_STKPUSHQUERY_QUERY),
            headers={"Authorization": f"Bearer {access_token or self.access_token}"},
            json=payload,
        )
        result_dict = self._make_result(response)
        if response.status_code != 200:
            return STKPushQueryErrorResult(**result_dict)
        return STKPushQueryResult(**result_dict)

    def _generate_password(
        self,
        business_short_code: Union[str, int],
        pass_key: Optional[str],
        timestamp: Optional[str],
    ) -> Tuple[str, str]:
        if not timestamp:
            timestamp = str_now()
        return (
            generate_password(
                business_short_code=business_short_code,
                pass_key=pass_key or "",
                timestamp=timestamp,
            ),
            timestamp,
        )

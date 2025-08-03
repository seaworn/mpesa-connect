from dataclasses import dataclass
from typing import Optional, Union

import requests

from .app import AppEnv
from .base import API, ErrorResult, Result
from .enums import CommandID, ResponseType
from .urls import PATH_C2B_REGISTERURL, PATH_C2B_SIMULATE


@dataclass
class C2BResult(Result):
    originator_conversation_id: str
    response_code: str
    response_description: str


@dataclass
class C2BErrorResult(ErrorResult):
    pass


@dataclass
class C2BSimulateResult(Result):
    pass


@dataclass
class C2BSimulateErrorResult(ErrorResult):
    pass


class C2B(API):
    def register_url(
        self,
        *,
        short_code: Union[str, int],
        validation_url: str,
        confirmation_url: str,
        response_type: Union[ResponseType, str],
        access_token: Optional[str] = None,
    ) -> Union[C2BResult, C2BErrorResult]:
        payload = {
            "ShortCode": short_code,
            "ValidationURL": validation_url,
            "ConfirmationURL": confirmation_url,
            "ResponseType": (
                response_type.value
                if isinstance(response_type, ResponseType)
                else response_type
            ),
        }
        response = requests.post(
            self.get_url(PATH_C2B_REGISTERURL),
            headers={"Authorization": f"Bearer {access_token or self.access_token}"},
            json=payload,
        )
        result_dict = self._make_result(response)
        if response.status_code != 200:
            return C2BErrorResult(**result_dict)
        return C2BResult(**result_dict)

    def simulate(
        self,
        *,
        short_code: Union[str, int],
        command_id: Union[CommandID, str],
        amount: Union[str, int],
        msisdn: Union[str, int],
        bill_ref_number: Optional[str] = None,
        access_token: Optional[str] = None,
    ) -> Union[C2BSimulateResult, C2BSimulateErrorResult]:
        if self.app.env != AppEnv.SANDBOX:
            raise Exception("Simulate is available on sandbox only")
        if isinstance(command_id, CommandID):
            command_id = command_id.value
        payload = {
            "ShortCode": short_code,
            "CommandID": command_id,
            "Amount": amount,
            "Msisdn": msisdn,
            "BillRefNumber": bill_ref_number,
        }
        response = requests.post(
            self.get_url(PATH_C2B_SIMULATE),
            headers={"Authorization": f"Bearer {access_token or self.access_token}"},
            json=payload,
        )
        result_dict = self._make_result(response)
        if response.status_code != 200:
            return C2BSimulateErrorResult(**result_dict)
        return C2BSimulateResult(**result_dict)

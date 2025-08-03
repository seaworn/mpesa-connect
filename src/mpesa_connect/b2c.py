from dataclasses import dataclass
from typing import Optional, Union

import requests

from .base import API, ErrorResult, Result
from .enums import CommandID
from .urls import PATH_B2C_PAYMENTREQUEST


@dataclass
class B2CResult(Result):
    conversation_id: str
    originator_conversation_id: str
    response_code: str
    response_description: str


@dataclass
class B2CErrorResult(ErrorResult):
    pass


class B2C(API):
    def payment_request(
        self,
        *,
        originator_conversation_id: str,
        initiator_name: str,
        security_credential: str,
        command_id: Union[CommandID, str],
        amount: Union[str, int],
        party_a: Union[str, int],
        party_b: Union[str, int],
        remarks: str,
        queue_time_out_url: str,
        result_url: str,
        occassion: Optional[str] = None,
        access_token: Optional[str] = None,
    ) -> Union[B2CResult, B2CErrorResult]:
        payload = {
            "OriginatorConversationID": originator_conversation_id,
            "InitiatorName": initiator_name,
            "SecurityCredential": security_credential,
            "CommandID": (
                command_id.value if isinstance(command_id, CommandID) else command_id
            ),
            "Amount": amount,
            "PartyA": party_a,
            "PartyB": party_b,
            "Remarks": remarks,
            "QueueTimeOutURL": queue_time_out_url,
            "ResultURL": result_url,
            "Occassion": occassion or "",
        }
        response = requests.post(
            self.get_url(PATH_B2C_PAYMENTREQUEST),
            headers={"Authorization": f"Bearer {access_token or self.access_token}"},
            json=payload,
        )
        result_dict = self._make_result(response)
        if response.status_code != 200:
            return B2CErrorResult(**result_dict)
        return B2CResult(**result_dict)

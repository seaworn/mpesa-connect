from dataclasses import dataclass
from typing import Optional, Union

import requests

from .base import API, ErrorResult, Result
from .enums import CommandID
from .urls import PATH_REVERSAL_REQUEST


@dataclass
class ReversalResult(Result):
    originator_conversation_id: str
    conversation_id: str
    response_code: str
    response_description: str


@dataclass
class ReversalErrorResult(ErrorResult):
    pass


class Reversal(API):
    def request(
        self,
        *,
        initiator: str,
        security_credential: str,
        command_id: Union[CommandID, str] = CommandID.TRANSACTION_REVERSAL,
        transaction_id: str,
        amount: Union[str, int],
        receiver_party: Union[str, int],
        receiver_identifier_type: Union[str, int],
        result_url: str,
        queue_time_out_url: str,
        remarks: str,
        occasion: str = "",
        access_token: Optional[str] = None,
    ) -> Union[ReversalResult, ReversalErrorResult]:
        payload = {
            "Initiator": initiator,
            "SecurityCredential": security_credential,
            "CommandID": (
                command_id.value if isinstance(command_id, CommandID) else command_id
            ),
            "TransactionID": transaction_id,
            "Amount": amount,
            "ReceiverParty": receiver_party,
            "RecieverIdentifierType": receiver_identifier_type,
            "ResultURL": result_url,
            "QueueTimeOutURL": queue_time_out_url,
            "Remarks": remarks,
            "Occasion": occasion,
        }
        response = requests.post(
            self.get_url(PATH_REVERSAL_REQUEST),
            headers={"Authorization": f"Bearer {access_token or self.access_token}"},
            json=payload,
        )
        result_dict = self._make_result(response)
        if response.status_code != 200:
            return ReversalErrorResult(**result_dict)
        return ReversalResult(**result_dict)

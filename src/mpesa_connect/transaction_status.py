from dataclasses import dataclass
from typing import Optional, Union

import requests

from .base import API, ErrorResult, Result
from .enums import CommandID, IdentifierType
from .urls import PATH_TRANSACTIONSTATUS_QUERY


@dataclass
class TransactionStatusResult(Result):
    conversation_id: str
    originator_conversation_id: str
    response_code: str
    response_description: str


@dataclass
class TransactionStatusErrorResult(ErrorResult):
    pass


class TransactionStatus(API):
    def query(
        self,
        *,
        originator_conversation_id: str,
        initiator: str,
        security_credential: str,
        transaction_id: str,
        identifier_type: Union[IdentifierType, str, int],
        party_a: Union[str, int],
        remarks: str,
        queue_time_out_url: str,
        result_url: str,
        command_id: Union[CommandID, str] = CommandID.TRANSACTION_STATUS_QUERY,
        occassion: Optional[str] = None,
        access_token: Optional[str] = None,
    ) -> Union[TransactionStatusResult, TransactionStatusErrorResult]:
        payload = {
            "OriginatorConversationID": originator_conversation_id,
            "Initiator": initiator,
            "SecurityCredential": security_credential,
            "CommandID": (
                command_id.value if isinstance(command_id, CommandID) else command_id
            ),
            "TransactionID": transaction_id,
            "PartyA": party_a,
            "IdentifierType": (
                identifier_type.value
                if isinstance(identifier_type, IdentifierType)
                else identifier_type
            ),
            "Remarks": remarks,
            "QueueTimeOutURL": queue_time_out_url,
            "ResultURL": result_url,
            "Occassion": occassion,
        }
        response = requests.post(
            self.get_url(PATH_TRANSACTIONSTATUS_QUERY),
            headers={"Authorization": f"Bearer {access_token or self.access_token}"},
            json=payload,
        )
        result_dict = self._make_result(response)
        if response.status_code != 200:
            return TransactionStatusErrorResult(**result_dict)
        return TransactionStatusResult(**result_dict)

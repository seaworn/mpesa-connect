from dataclasses import dataclass
from typing import Optional, Union

import requests

from .base import API, ErrorResult, Result
from .enums import CommandID, IdentifierType
from .urls import PATH_ACCOUNTBALANCE_QUERY


@dataclass
class AccountBalanceResult(Result):
    originator_conversation_id: str
    conversation_id: str
    response_code: str
    response_description: str


@dataclass
class AccountBalanceErrorResult(ErrorResult):
    pass


class AccountBalance(API):
    def query(
        self,
        *,
        initiator: str,
        security_credential: str,
        identifier_type: Union[IdentifierType, str, int],
        party_a: Union[str, int],
        remarks: str,
        queue_time_out_url: str,
        result_url: str,
        command_id: Union[CommandID, str] = CommandID.ACCOUNT_BALANCE,
        access_token: Optional[str] = None,
    ) -> Union[AccountBalanceResult, AccountBalanceErrorResult]:
        payload = {
            "Initiator": initiator,
            "SecurityCredential": security_credential,
            "CommandID": (
                command_id.value if isinstance(command_id, CommandID) else command_id
            ),
            "PartyA": party_a,
            "IdentifierType": (
                identifier_type.value
                if isinstance(identifier_type, IdentifierType)
                else identifier_type
            ),
            "Remarks": remarks,
            "QueueTimeOutURL": queue_time_out_url,
            "ResultURL": result_url,
        }
        response = requests.post(
            self.get_url(PATH_ACCOUNTBALANCE_QUERY),
            headers={"Authorization": f"Bearer {access_token or self.access_token}"},
            json=payload,
        )
        result_dict = self._make_result(response)
        if response.status_code != 200:
            return AccountBalanceErrorResult(**result_dict)
        return AccountBalanceResult(**result_dict)

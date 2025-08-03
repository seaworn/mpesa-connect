from dataclasses import dataclass
from typing import Optional, Union

import requests

from .base import API, ErrorResult, Result
from .enums import TrxCode
from .urls import PATH_QRCODE_GENERATE


@dataclass
class QRCodeResult(Result):
    response_code: str
    response_description: str
    qr_code: str


@dataclass
class QRCodeErrorResult(ErrorResult):
    pass


class QRCode(API):
    def generate(
        self,
        *,
        merchant_name: str,
        ref_no: str,
        amount: Union[str, int],
        trx_code: Union[TrxCode, str],
        cpi: str,
        size: Union[str, int],
        access_token: Optional[str] = None,
    ) -> Union[QRCodeResult, QRCodeErrorResult]:
        payload = {
            "MerchantName": merchant_name,
            "RefNo": ref_no,
            "Amount": amount,
            "TrxCode": trx_code.value if isinstance(trx_code, TrxCode) else trx_code,
            "CPI": cpi,
            "Size": size,
        }
        response = requests.post(
            self.get_url(PATH_QRCODE_GENERATE),
            headers={"Authorization": f"Bearer {access_token or self.access_token}"},
            json=payload,
        )
        result_dict = self._make_result(response)
        if response.status_code != 200:
            return QRCodeErrorResult(**result_dict)
        return QRCodeResult(**result_dict)

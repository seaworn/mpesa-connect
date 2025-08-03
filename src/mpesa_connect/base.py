import logging
from dataclasses import dataclass
from typing import Any, Dict, Literal, Optional
from urllib.parse import urljoin

import requests

from .app import App
from .utils import convert_to_snake_case

_logger = logging.getLogger(__name__)


@dataclass
class Result:
    response: requests.Response
    status_ok: Literal[True]


@dataclass
class ErrorResult:
    response: requests.Response
    status_ok: Literal[False]
    request_id: str
    error_code: str
    error_message: str


class API:
    def __init__(
        self,
        app: App,
        /,
        *,
        access_token: Optional[str] = None,
    ) -> None:
        self.app = app
        self.access_token = access_token

    def get_url(self, path: str) -> str:
        return urljoin(self.app.base_url, path)

    def _make_result(self, response: requests.Response) -> Dict[str, Any]:
        try:
            json = response.json()
        except requests.JSONDecodeError as e:
            _logger.error(str(e))
            raise e
        result = {convert_to_snake_case(k): v for k, v in json.items()}
        result["response"] = response
        result["status_ok"] = response.status_code == 200
        return result

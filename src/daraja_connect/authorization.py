from typing import Any
from urllib.parse import urljoin

import requests

from .base import Service
from .urls import PATH_OAUTH_GENERATE
from .utils import base64encode


class Authorization(Service):
    def generate_token(self) -> Any:
        credentials = base64encode(
            f"{self.app.consumer_key}:{self.app.consumer_secret}"
        )
        response = requests.get(
            urljoin(self.app.base_url, PATH_OAUTH_GENERATE),
            headers={"Authorization": f"Basic {credentials}"},
        )
        return self._make_result(response)

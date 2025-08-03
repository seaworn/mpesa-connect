from dataclasses import dataclass
from typing import Union

import requests
from requests.auth import HTTPBasicAuth

from .app import App
from .base import API, ErrorResult, Result
from .urls import PATH_OAUTH_GENERATE


@dataclass
class OAuthResult(Result):
    access_token: str
    expires_in: str


@dataclass
class OAuthErrorResult(ErrorResult):
    pass


class OAuth(API):
    def __init__(self, app: App, /):
        self.app = app

    def generate(self) -> Union[OAuthResult, OAuthErrorResult]:
        response = requests.get(
            self.get_url(PATH_OAUTH_GENERATE),
            {"grant_type": "client_credentials"},
            auth=HTTPBasicAuth(self.app.consumer_key, self.app.consumer_secret),
        )
        result_dict = self._make_result(response)
        if response.status_code != 200:
            return OAuthErrorResult(**result_dict)
        return OAuthResult(**result_dict)

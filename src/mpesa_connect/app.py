from enum import Enum
from typing import Any, Literal, Union

from .urls import LIVE_URL, SANDBOX_URL


class AppEnv(Enum):
    LIVE = LIVE_URL
    SANDBOX = SANDBOX_URL


class App:
    def __init__(
        self,
        *,
        env: Union[AppEnv, Literal["sandbox", "live"]],
        consumer_key: str,
        consumer_secret: str,
    ) -> None:
        self.env = AppEnv[env.upper()] if isinstance(env, str) else env
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret

    @property
    def base_url(self):
        return self.env.value

    @classmethod
    def create_sandbox(cls, **kwargs: Any) -> "App":
        return cls(env=AppEnv.SANDBOX, **kwargs)

    @classmethod
    def create_live(cls, **kwargs: Any) -> "App":
        return cls(env=AppEnv.LIVE, **kwargs)

import re

import pytest

from mpesa_connect.utils import convert_to_snake_case, str_now


def test_str_now() -> None:
    assert re.match(r"^\d{4}\d{2}\d{2}\d{2}\d{2}\d{2}$", str_now()) is not None


@pytest.mark.parametrize(
    "input,output",
    [
        ("snake_case", "snake_case"),
        ("snake123", "snake123"),
        ("SnakeCase", "snake_case"),
        ("ABCSnakeCase", "abc_snake_case"),
        ("snakeCaseABC", "snake_case_abc"),
    ],
)
def test_snake_case(input: str, output: str) -> None:
    assert convert_to_snake_case(input) == output

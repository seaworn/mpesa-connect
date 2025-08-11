import base64
import logging
import pathlib
import re
from datetime import datetime
from typing import Union

_logger = logging.getLogger(__name__)


def base64encode(data: str) -> str:
    return base64.b64encode(data.encode("utf8")).decode("utf8")


def str_now() -> str:
    return datetime.now().strftime("%Y%m%d%H%M%S")


def convert_to_snake_case(str: str) -> str:
    return re.sub(r"((?<=[a-z0-9])[A-Z]|(?!^)[A-Z](?=[a-z]))", r"_\1", str).lower()


def generate_password(
    *,
    business_short_code: Union[int, str],
    pass_key: str,
    timestamp: Union[str, int],
) -> str:
    return base64encode(str(business_short_code) + pass_key + str(timestamp))


def generate_security_credential(
    password: str, cer: Union[pathlib.Path, str, bytes]
) -> str:
    """
    Generate security credentials from a PEM certificate

    Args:
        password (str): The unencrypted initiator password
        cert (str): X509 certificate - either the path to a file or the PEM string in bytes

    Returns:
        str: Base64 encoded security credential
    """
    try:
        from cryptography import x509
        from cryptography.hazmat.primitives.asymmetric import padding
    except ImportError as e:
        _logger.error(str(e))
        raise Exception(
            "Cryptography library is not installed, please install with `pip install mpesa-connect[cryptography]`"
        ) from e
    try:
        # Read the certificate
        if isinstance(cer, pathlib.Path):
            with cer.open("rb") as f:
                data = f.read()
        elif isinstance(cer, str):
            with open(cer, "rb") as f:
                data = f.read()
        else:
            data = cer
        # Extract public key
        certificate = x509.load_pem_x509_certificate(data)
        public_key = certificate.public_key()
        # Encrypt using RSA with PKCS1v1.5 padding
        encrypted_bytes = public_key.encrypt(password.encode(), padding.PKCS1v15())
        # Convert to base64 string
        return base64.b64encode(encrypted_bytes).decode()
    except Exception as e:
        _logger.error(str(e))
        raise Exception(f"Error generating security credential: {str(e)}") from e

from typing import Final

SANDBOX_URL: Final[str] = "https://sandbox.safaricom.co.ke"
LIVE_URL: Final[str] = "https://api.safaricom.co.ke"
PATH_OAUTH_GENERATE: Final[str] = "/oauth/v1/generate"
PATH_STKPUSH_PROCESSREQUEST: Final[str] = "/mpesa/stkpush/v1/processrequest"
PATH_STKPUSHQUERY_QUERY: Final[str] = "/mpesa/stkpushquery/v1/query"
PATH_C2B_REGISTERURL: Final[str] = "/mpesa/c2b/v1/registerurl"
PATH_C2B_SIMULATE: Final[str] = "/mpesa/c2b/v1/simulate"
PATH_B2C_PAYMENTREQUEST: Final[str] = "/mpesa/b2c/v1/paymentrequest"
PATH_TRANSACTIONSTATUS_QUERY: Final[str] = "/mpesa/transactionstatus/v1/query"
PATH_ACCOUNTBALANCE_QUERY: Final[str] = "/mpesa/accountbalance/v1/query"
PATH_QRCODE_GENERATE: Final[str] = "/mpesa/qrcode/v1/generate"

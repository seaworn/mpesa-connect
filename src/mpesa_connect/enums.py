from enum import Enum


class TransactionType(Enum):
    CUSTOMER_BUY_GOODS_ONLINE = "CustomerBuyGoodsOnline"
    CUSTOMER_PAY_BILL_ONLINE = "CustomerPayBillOnline"


class CommandID(Enum):
    BUSINESS_PAYMENT = "BusinessPayment"
    SALARY_PAYMENT = "SalaryPayment"
    PROMOTION_PAYMENT = "PromotionPayment"
    ACCOUNT_BALANCE = "AccountBalance"
    TRANSACTION_STATUS_QUERY = "TransactionStatusQuery"


class ResponseType(Enum):
    COMPLETED = "Completed"
    CANCELED = "Canceled"


class IdentifierType(Enum):
    MSISDN = 1
    TILL_NUMBER = 2
    ORGANIZATION_SHORT_CODE = 4


class TrxCode(Enum):
    BG = "BG"
    PB = "PB"
    SB = "SB"
    SM = "SM"
    WA = "WA"

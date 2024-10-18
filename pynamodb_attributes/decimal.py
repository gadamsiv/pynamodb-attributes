import decimal
from pynamodb.attributes import Attribute
from pynamodb.attributes import NumberAttribute


DYNAMODB_CONTEXT = decimal.Context(
    Emin=-128, Emax=126, rounding=None, prec=38,
    traps=[
        decimal.Clamped,
        decimal.Overflow,
        decimal.Inexact,
        decimal.Rounded,
        decimal.Underflow
    ]
)


class DecimalAttribute(Attribute[decimal.Decimal]):
    """
    Serialize and deserialize decimal.Decimal instances with a given decimal.Context.

    The default decimal.Context comes from the definition used by boto3.
    """
    
    attr_type = NumberAttribute.attr_type
    
    def __init__(self, context=None):
        context = context or DYNAMODB_CONTEXT
        self.context = context

    def serialize(self, value):
        # decimal.Decimal -> str
        return str(self.context.create_decimal(value))

    def deserialize(self, value):
        # str -> decimal.Decimal
        return self.context.create_decimal(value)
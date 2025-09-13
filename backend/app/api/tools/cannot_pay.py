from enum import Enum


class PaymentFailureType(Enum):
    TERMINAL_NOT_WORKING = "TERMINAL_NOT_WORKING"
    NO_TERMINAL_AT_EXIT = "NO_TERMINAL_AT_EXIT"
    DONT_HAVE_PAYMENT_CARD = "DONT_HAVE_PAYMENT_CARD"




class CannotPayTool:

    @staticmethod
    def execute(
        payment_failure_type: PaymentFailureType,
    ) -> str:
        if payment_failure_type == PaymentFailureType.TERMINAL_NOT_WORKING:
            return "The payment terminal is currently not working. Please proceed to the nearest payment kiosk or contact support for assistance."
        elif payment_failure_type == PaymentFailureType.NO_TERMINAL_AT_EXIT:
            return "There is no payment terminal at this exit. Please proceed to the nearest payment kiosk or contact support for assistance."
        elif payment_failure_type == PaymentFailureType.DONT_HAVE_PAYMENT_CARD:
            return "You do not have a payment card with you. Please proceed to the nearest payment kiosk or contact support for assistance."
        else:
            return "An unknown payment issue has occurred. Please contact support for assistance."


tool_description = {
    "type": "function",
    "function": {
        "name": "cannot_pay",
        "description": "Get active parking session information for a specific license plate number. Use this when a customer mentions their license plate and needs help with parking.",
        "parameters": {
            "type": "object",
            "properties": {
                "license_plate": {
                    "type": "string",
                    "description": "The license plate number to search for (e.g., 'ABC123')"
                },
            },
            "required": ["license_plate"],
            "additionalProperties": False
        },
        "strict": True
    }
}
from datetime import datetime

from app.api.repositories import get_session_repository, SessionRepository, get_payment_repository, PaymentRepository
from app.config.logging import logging

logger = logging.getLogger('customer_payment_failed_tool')


tool_name = "customer_payment_failed"


class CustomerPaymentFailedTool:

    def __init__(
        self,
        session_repository: SessionRepository = None,
        payment_repository: PaymentRepository = None
    ):
        self.session_repository = session_repository or get_session_repository()
        self.payment_repository = payment_repository or get_payment_repository()

    def execute(
        self,
        license_plate: str
    ) -> str:
        try:
            session = self.session_repository.get_session_by_license_plate(license_plate)
            if isinstance(session, Exception):
                logger.info(f"Error retrieving session for license plate {license_plate}: {str(session)}")
                return f"Error retrieving session for license plate {license_plate}: {str(session)}. Call the helpdesk for further assistance."
            if session is None:
                logger.info(f"No active session found for license plate {license_plate}")
                return f"No active session found for license plate {license_plate}. Call the helpdesk for further assistance."

            payment = self.payment_repository.get_payment_by_session_id(session.id)
            if isinstance(payment, Exception):
                logger.info(f"Error retrieving payment for license plate {license_plate}: {str(payment)}")
                return f"Error retrieving payment for license plate {license_plate}: {str(payment)}. Call the helpdesk for further assistance."
            if payment is None:
                logger.info(f"No payment record found for license plate {license_plate}")
                return f"No payment record found for license plate {license_plate}. Please complete the payment or call the helpdesk for further assistance."

            if not payment.approved:
                logger.info(f"Payment for license plate {license_plate} was declined")
                return f"Payment for license plate {license_plate} was declined. Please try another payment method or call the helpdesk for further assistance."
            if session.amount_due_cents > session.amount_paid_cents:
                logger.info(
                    f"Outstanding balance for license plate {license_plate}: {(session.amount_due_cents - session.amount_paid_cents) / 100:.2f}")
                return f"You still owe {(session.amount_due_cents - session.amount_paid_cents) / 100:.2f}. Please complete the payment or call the helpdesk for further assistance."

            logger.info(f"Payment for license plate {license_plate} was successful")

            self.session_repository.close_session(license_plate=license_plate, exit_license_plate=license_plate,
                exit_station=2,  # TODO: Fix later
                exit_time=datetime.now())

            return f"Payment for license plate {license_plate} was successful. You may proceed to exit."
        except Exception as e:
            logger.error(f"Unexpected error for license plate {license_plate}: {str(e)}")
            return f"Unexpected error for license plate {license_plate}: {str(e)}. Call the helpdesk for further assistance."


tool_description = {
    "type": "function",
    "function": {
        "name": tool_name,
        "description": """
            Should be used when payment is not found in the system, while the customer claims that he did pay.
            Verify the payment status for a specific license plate number
        """,
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
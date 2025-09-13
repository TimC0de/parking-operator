from datetime import datetime

from app.api.repositories import get_session_repository, SessionRepository
from app.config.logging import logging

logger = logging.getLogger('lost_ticket_tool')


tool_name = "lost_ticket"


class LostTicketTool:

    def __init__(
        self,
        session_repository: SessionRepository = None
    ):
        self.session_repository = session_repository or get_session_repository()

    def execute(
        self,
        license_plate: str,
    ) -> str:
        try:
            session = self.session_repository.get_session_by_license_plate(license_plate)
            if isinstance(session, Exception):
                logger.info(f"Error retrieving session for license plate {license_plate}: {str(session)}")
                return f"Error retrieving session for license plate {license_plate}: {str(session)}. Call the helpdesk for further assistance."
            if session is None:
                logger.info(f"No active session found for license plate {license_plate}")
                return f"No active session found for license plate {license_plate}. Call the helpdesk for further assistance."

            if session.amount_due_cents > session.amount_paid_cents:
                logger.info(f"Outstanding balance for license plate {license_plate}: {(session.amount_due_cents - session.amount_paid_cents) / 100:.2f}")
                return f"An active session was found for license plate {license_plate}, but there is an outstanding balance of {(session.amount_due_cents - session.amount_paid_cents) / 100:.2f}. Please proceed to payment or call the helpdesk for further assistance."

            self.session_repository.close_session(
                license_plate=license_plate,
                exit_license_plate=license_plate,
                exit_station=2,  # TODO: Fix later
                exit_time=datetime.now()
            )

            logger.info(f"Payment for license plate {license_plate} was successful")
            return f"An active session was found for license plate {license_plate} with no outstanding balance. You may proceed to exit."
        except Exception as e:
            logger.error(f"Unexpected error for license plate {license_plate}: {str(e)}")
            return f"Unexpected error for license plate {license_plate}: {str(e)}. Call the helpdesk for further assistance."


tool_description = {
    "type": "function",
    "function": {
        "name": tool_name,
        "description": """
            Should be used when the client says that he lost his parking ticket or simply asks for a new one.
            Assist a customer who has lost their parking ticket by asking their license plate number and checking for an active session.
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
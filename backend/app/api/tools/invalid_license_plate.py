from datetime import datetime

from app.api.service import get_session_service, SessionService
from app.config.logging import logging

logger = logging.getLogger('invalid_license_plate_tool')


tool_name = "invalid_license_plate"


class InvalidLicensePlateTool:

    def __init__(
        self,
        session_service: SessionService = None
    ):
        self.session_service = session_service or get_session_service()

    def execute(
        self,
        license_plate: str,
        entry_time_interval: (str, str),
        entry_station: int,
    ) -> str:
        try:
            session = self.session_service.get_similar_by_license_plate_entry_time_interval_and_entry_station(
                license_plate, entry_time_interval, entry_station)

            if isinstance(session, Exception):
                logger.info(f"Error retrieving session for license plate {license_plate}: {str(session)}")
                return f"Error retrieving session for license plate {license_plate}: {str(session)}. Call the helpdesk for further assistance."
            if session is None:
                logger.info(f"No active session found for license plate {license_plate}")
                return f"No active session found for license plate {license_plate}. Call the helpdesk for further assistance."

            if session.amount_due_cents > session.amount_paid_cents:
                logger.info(f"Outstanding balance for license plate {license_plate}: {(session.amount_due_cents - session.amount_paid_cents) / 100:.2f}")
                return f"An active session was found for license plate {license_plate}, but there is an outstanding balance of {(session.amount_due_cents - session.amount_paid_cents) / 100:.2f}. Please proceed to payment or call the helpdesk for further assistance."

            session_repository = self.session_service.session_repository
            session_repository.close_session(license_plate=session.licence_plate_entry,
                exit_license_plate=license_plate, exit_station=2,  # TODO: Fix later
                exit_time=datetime.now())

            if session.licence_plate_entry != license_plate:
                logger.info(f"License plate corrected from {license_plate} to {session.licence_plate_entry}")
                return f"There was a little mistake in license plate. We fixed it to your license plate: {license_plate}. You may proceed to exit."
            else:
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
            Should be used when the client's session is not found due to plate number mismatch on entry and exit gates.
            Assist a customer who entered a ticket-less gate and had their license plate number scanned incorrectly by the camera by asking their license plate number, entry time, and entered gate, and checking for an active session with these details. The goal is to find a session with similar details to identify the session with an incorrectly identified license plate number.
        """,
        "parameters": {
            "type": "object",
            "properties": {
                "license_plate": {
                    "type": "string",
                    "description": "The license plate number to search for (e.g., 'ABC123')"
                },
                "entry_time_interval": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "format": "date-time"
                    },
                    "minItems": 2,
                    "maxItems": 2,
                    "description": "The entry time interval (start and end) to search within (e.g., ['2023-10-01T08:00:00', '2023-10-01T10:00:00'])"
                },
                "entry_station": {
                    "type": "integer",
                    "description": "The entry station ID where the vehicle entered (e.g., 1)"
                },
            },
            "required": ["license_plate", "entry_time_interval", "entry_station"],
            "additionalProperties": False
        },
        "strict": True
    }
}

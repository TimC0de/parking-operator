from app.api.service import get_session_service, SessionService


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
        session = self.session_service.get_similar_by_license_plate_entry_time_interval_and_entry_station(
            license_plate,
            entry_time_interval,
            entry_station
        )

        if isinstance(session, Exception):
            return f"Error retrieving session for license plate {license_plate}: {str(session)}. Call the helpdesk for further assistance."
        if session is None:
            return f"No active session found for license plate {license_plate}. Call the helpdesk for further assistance."

        if session.amount_due_cents > session.amount_paid_cents:
            return f"An active session was found for license plate {license_plate}, but there is an outstanding balance of {(session.amount_due_cents - session.amount_paid_cents) / 100:.2f}. Please proceed to payment or call the helpdesk for further assistance."

        if session.licence_plate_entry != license_plate:
            # TODO: Fix license plate
            return f"THere was a little mistake in license plate. We fixed it to your license plate: {license_plate}. You may proceed to exit."

        return f"An active session was found for license plate {license_plate} with no outstanding balance. You may proceed to exit."


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

from app.api.repositories import get_session_repository, SessionRepository


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
        session = self.session_repository.get_session_by_license_plate(license_plate)
        if isinstance(session, Exception):
            return f"Error retrieving session for license plate {license_plate}: {str(session)}. Call the helpdesk for further assistance."
        if session is None:
            return f"No active session found for license plate {license_plate}. Call the helpdesk for further assistance."

        if session.amount_due_cents > session.amount_paid_cents:
            return f"An active session was found for license plate {license_plate}, but there is an outstanding balance of {(session.amount_due_cents - session.amount_paid_cents) / 100:.2f}. Please proceed to payment or call the helpdesk for further assistance."

        return f"An active session was found for license plate {license_plate} with no outstanding balance. You may proceed to exit."


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
from app.api.tools import customer_payment_failed, lost_ticket, invalid_license_plate

tools = [
    customer_payment_failed.tool_description,
    lost_ticket.tool_description,
    invalid_license_plate.tool_description
]
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Payment:
    id: int
    session_id: int
    station_id: int
    method: str
    amount_cents: int
    approved: bool
    processor_ref: str
    created_at: datetime
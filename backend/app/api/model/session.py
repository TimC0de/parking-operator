from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional


class SessionStatus(Enum):
    ACTIVE = 'active'
    EXITED = 'exited'


@dataclass
class Session:
    id: int
    ticket_id: Optional[int]
    entry_time: datetime
    entry_station: int
    exit_time: Optional[datetime]
    exit_station: Optional[int]
    status: str
    amount_due_cents: int
    amount_paid_cents: int
    paid_until: Optional[datetime]
    licence_plate_entry: Optional[str]
    licence_plate_exit: Optional[str]

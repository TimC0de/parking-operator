import config

from .payment_repository import PaymentRepository
from .session_repository import SessionRepository


def get_session_repository():
    return SessionRepository(config.env_param('SQLITE_DATABASE_NAME'))


def get_payment_repository():
    return PaymentRepository(config.env_param('SQLITE_DATABASE_NAME'))
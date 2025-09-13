from typing import Union, Optional

from app.config.logging import logging
import sqlite3

from app.api.model.payment import Payment

logger = logging.getLogger('payment_repository')


class PaymentRepository:

    def __init__(self, db_name):
        self.db_name = db_name
        self.db_connection = sqlite3.connect(self.db_name)

    def __del__(self):
        if self.db_connection:
            self.db_connection.close()

    def get_payment_by_session_id(
        self,
        session_id: int,
    ) -> Union[Optional[Payment], Exception]:
        query = """
            SELECT *
            FROM payment
            WHERE session_id = ?
            """

        try:
            cursor = self.db_connection.cursor()
            cursor.execute(
                query,
                (session_id,)
            )
            result = cursor.fetchone()

            if not result:
                return None

            logger.info(f"Payment found for session ID {session_id}: {result}")

            return Payment(*result)
        except sqlite3.Error as e:
            logger.info(f"Database error for session ID {session_id}: {str(e)}")
            return Exception('Database error: {str(e)}')
        except Exception as e:
            logger.info(f"Unexpected error for session ID {session_id}: {str(e)}")
            return e
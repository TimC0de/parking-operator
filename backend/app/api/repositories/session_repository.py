import json
import sqlite3
from datetime import datetime
from typing import Optional, Union

from app.api.model.session import Session

from app.config.logging import logging

logger = logging.getLogger('session_repository')


class SessionRepository:

    def __init__(self, db_name):
        self.db_name = db_name
        self.db_connection = sqlite3.connect(self.db_name)

    def __del__(self):
        if self.db_connection:
            self.db_connection.close()

    def get_session_by_license_plate(
        self,
        license_plate: str,
    ) -> Union[Optional[Session], Exception]:
        query = """
            SELECT *
            FROM session
            WHERE UPPER(licence_plate_entry) = UPPER(?)
            AND status = 'active'
            ORDER BY entry_time DESC
            """

        try:
            cursor = self.db_connection.cursor()
            cursor.execute(
                query,
                (license_plate,)
            )
            result = cursor.fetchone()

            logger.info(f"Executed query for license plate {license_plate}")

            if not result:
                return None

            logger.info(f"Session found for license plate {license_plate}: {result}")

            return Session(*result)
        except sqlite3.Error as e:
            logger.info(f"Database error for license plate {license_plate}: {str(e)}")
            return Exception('Database error: {str(e)}')
        except Exception as e:
            logger.info(f"Unexpected error for license plate {license_plate}: {str(e)}")
            return e

    def get_session_by_entry_time_and_entry_station(
        self,
        entry_time: datetime,
        entry_station: int
    ) -> Union[list[Session], Exception]:
        query = """
            SELECT *
            FROM session
            WHERE entry_time = ?
            AND entry_station = ?
            AND status = 'active'
            ORDER BY entry_time DESC
            """

        try:
            cursor = self.db_connection.cursor()
            cursor.execute(
                query,
                (
                    entry_time,
                    entry_station
                )
            )
            result = cursor.fetchall()
            if not result:
                return []

            return [Session(*row) for row in result]
        except sqlite3.Error as e:
            logger.info(f"Database error for entry_time {entry_time} and entry_station {entry_station}: {str(e)}")
            return Exception(f'Database error: {str(e)}')
        except Exception as e:
            logger.info(f"Unexpected error for entry_time {entry_time} and entry_station {entry_station}: {str(e)}")
            return e

    def get_session_by_entry_time_interval_and_entry_station(
        self,
        entry_time_interval: (datetime, datetime),
        entry_station: int,
    ) -> Union[list[Session], Exception]:
        query = """
            SELECT *
            FROM session
            WHERE entry_time BETWEEN ? AND ?
            AND entry_station = ?
            AND status = 'active'
            ORDER BY entry_time DESC
            """

        try:
            cursor = self.db_connection.cursor()
            cursor.execute(
                query,
                (
                    entry_time_interval[0],
                    entry_time_interval[1],
                    entry_station
                )
            )
            results = cursor.fetchall()
            if not results:
                return []

            return [Session(*row) for row in results]
        except sqlite3.Error as e:
            logger.info(f"Database error for entry_time interval {entry_time_interval} and entry_station {entry_station}: {str(e)}")
            return Exception(f'Database error: {str(e)}')
        except Exception as e:
            logger.info(f"Unexpected error for entry_time interval {entry_time_interval} and entry_station {entry_station}: {str(e)}")
            return e

    def close_session(
        self,
        license_plate: str,
        exit_license_plate: str,
        exit_time: datetime,
        exit_station: int
    ) -> Union[Optional[Session], Exception]:
        query = """
            UPDATE session
            SET licence_plate_exit = ?,
                exit_time = ?,
                exit_station = ?,
                status = 'exited'
            WHERE UPPER(licence_plate_entry) = UPPER(?)
            AND status = 'active'
            ORDER BY entry_time DESC
            LIMIT 1
            """

        try:
            cursor = self.db_connection.cursor()
            cursor.execute(
                query,
                (
                    exit_license_plate,
                    exit_time,
                    exit_station,
                    license_plate
                )
            )
            self.db_connection.commit()

            if cursor.rowcount == 0:
                logger.info(f"No active session found to update for license plate {license_plate}")
                return None

            return self.get_session_by_license_plate(exit_license_plate)
        except sqlite3.Error as e:
            logger.info(f"Database error while updating session for license plate {license_plate}: {str(e)}")
            return Exception(f'Database error: {str(e)}')
        except Exception as e:
            logger.info(f"Unexpected error while updating session for license plate {license_plate}: {str(e)}")
            return e
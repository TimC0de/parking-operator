from app.config.logging import logging
from datetime import datetime
from typing import Union, Optional

from app.api.model.session import Session

from app.api.repositories import SessionRepository, get_session_repository

logger = logging.getLogger('session_service')


class SessionService:

    def __init__(self, session_repository: SessionRepository = None):
        self.session_repository = session_repository or get_session_repository()

    def _get_closest_license_plate(
        self,
        license_plate: str,
        sessions: list[Session]
    ) -> Union[Optional[Session], Exception]:
        license_plate_length = len(license_plate)
        similarities: list[(Session, int)] = []
        for session in sessions:
            similarities_score = 0

            for i in range(min(license_plate_length, len(session.licence_plate_entry))):
                if license_plate[i] == session.licence_plate_entry[i]:
                    similarities_score += 1

            similarities.append((session, similarities_score))

        similarities.sort(key=lambda x: x[1], reverse=True)
        closest_session, similarity_score = similarities[0] if len(similarities) > 0 else (None, 0)

        if similarity_score / len(license_plate) < 0.5:
            logger.info(
                f"No sufficiently similar session found for license plate {license_plate}")
            return Exception(
                f'No sufficiently similar session found for license plate {license_plate}')

        logger.info(
            f"Found similar session for license plate {license_plate}")

        return closest_session

    def get_similar_by_license_plate_entry_time_interval_and_entry_station(
        self,
        license_plate: str,
        entry_time_interval: (datetime, datetime),
        entry_station: int,
        **kwargs
    ) -> Union[Optional[Session], Exception]:
        try:
            result: Union[list[Session], Exception] = self.session_repository.get_session_by_entry_time_interval_and_entry_station(
                entry_time_interval,
                entry_station
            )

            if isinstance(result, list):
                if len(result) > 1:
                    closest_session = self._get_closest_license_plate(
                        license_plate,
                        result
                    )
                    return closest_session
                else:
                    return result[0] if len(result) == 1 else None

            return result
        except Exception as e:
            logger.info(f"Error retrieving similar sessions for license plate {license_plate}, entry_time_interval {entry_time_interval}, and entry_station {entry_station}: {str(e)}")
            return e

    def get_similar_by_license_plate_entry_time_and_entry_station(
        self,
        license_plate: str,
        entry_time: datetime,
        entry_station: int,
        **kwargs
    ) -> Union[Optional[Session], Exception]:
        try:
            result: Union[list[Session], Exception] = self.session_repository.get_session_by_entry_time_and_entry_station(
                entry_time,
                entry_station
            )

            if isinstance(result, list):
                if len(result) > 1:
                    closest_session = self._get_closest_license_plate(license_plate, result)
                    return closest_session
                else:
                    return result[0] if len(result) == 1 else None

            return result
        except Exception as e:
            logger.info(f"Error retrieving similar sessions for license plate {license_plate}, entry_time {entry_time}, and entry_station {entry_station}: {str(e)}")
            return e

    def get_session_by_license_plate(
        self,
        license_plate: str,
        **kwargs
    ) -> Union[Optional[Session], Exception]:
        try:
            result: Union[list[Session], Exception] = self.session_repository.get_session_by_license_plate(
                license_plate
            )

            return result
        except Exception as e:
            logger.info(f"Error retrieving sessions for license plate {license_plate}: {str(e)}")
            return e
from pydantic_settings import BaseSettings

import sportsradar


logger =  sportsradar.logging_helpers.get_logger(__name__)

class SportsRadarSettings(BaseSettings):
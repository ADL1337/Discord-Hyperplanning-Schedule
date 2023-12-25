from verifier import Verifier
from getter import Getter
from poster import Poster
from config import Config
from datetime import datetime


class Controller:
    def __init__(self, config_path):
        self.__config = Config(config_path)
        self.__getter = Getter(self.__config.section_id, self.__config.role_ids, self.current_week, self.__config.headless, self.__config.profile_path)
        self.__poster = Poster(self.__config.channels, self.__config.message_ids, self.__config.role_ids)

    @property
    def current_week(self) -> int:
        """Returns the current week of the school year
        by applying an offset to the actual current week of the year."""
        now = datetime.now().isocalendar()
        return (now.week + self.__config.week_offset) % 52 + (now.weekday > 5)

    def run(self):
        """Runs the bot"""
        schedules = self.__getter.run()
        self.__poster.post(schedules, self.current_week, Verifier.is_holiday(schedules[1]))

from yaml import safe_load


class Config:
    def __init__(self, config_path):
        self.__config = self.load_config(config_path)

    @staticmethod
    def load_config(config_path) -> dict:
        """Returns the config file as a dict"""
        with open(config_path, "r") as f:
            return safe_load(f)
    
    @property
    def profile_path(self) -> str:
        """Returns the path to the selenium profile"""
        return self.__config["profile_path"]

    @property
    def headless(self) -> bool:
        """Returns the headless mode of the selenium driver"""
        return self.__config["headless"]

    @property
    def week_offset(self) -> int:
        """Returns the week offset on hyperplanning compared to the current week"""
        return self.__config["week_offset"]

    @property
    def channels(self) -> dict:
        """Returns the channel ids of the channels where the bot will post the schedules"""
        return self.__config["channels"]

    @property
    def message_ids(self) -> dict:
        """Returns the ids of the messages that the bot will edit"""
        return self.__config["message_ids"]
    
    @property
    def role_ids(self) -> dict:
        """Returns the ids of the roles that the bot will ping"""
        return self.__config["roles"]
    
    @property
    def section_id(self) -> str:
        """Returns the corresponding id of the section on hyperplanning"""
        return str(self.__config["section_id"])
    
    @property
    def groups(self) -> list:
        return self.role_ids.keys()


if __name__ == "__main__":
    config = Config("live_config.yaml")
    print(config.section_id)
    print(config.role_ids)

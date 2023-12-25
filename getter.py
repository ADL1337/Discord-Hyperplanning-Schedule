from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from io import BytesIO
from time import sleep
from requests import head
from PIL import Image


class Getter:
    __schedule_url = "" # Replace with hyperplanning URL (could also load from config)
    __timeout = 60
    __wait_time = 1.6
    def __init__(self, section_id, group_ids, week, headless=False, profile_path=None):
        self.__section_id = section_id
        self.__group_ids = group_ids
        self.__week = week
        self.__headless = headless
        self.__profile_path = profile_path
        self.__driver = None
        self.__state = "1"
    
    def run(self) -> dict:
        """Runs the getter and returns the schedules as a dict of PIL Image objects"""
        self.__start_driver()
        schedules = self.__get_schedules()
        self.__close_driver()
        return schedules

    def __get_schedules(self) -> dict:
        """Returns the schedules of the groups as a dict"""
        schedules = {}
        for group_id in self.__group_ids:
            if self.__state == "F": schedules[group_id] = "F"; continue
            schedules[group_id] = self.__get_schedule(group_id)
        return schedules
    
    def __screenshot_schedule(self) -> Image:
        """Returns a screenshot of the schedule as a Image object"""
        res = Image.open(BytesIO(self.__driver.get_screenshot_as_png()))
        res = res.crop((0, 220, 1900, 930))
        return res

    def __get_schedule(self, group_id) -> BytesIO:
        """Returns the schedule of the group as a BytesIO object"""
        self.__select_group(group_id)
        return self.__screenshot_schedule()

    def __start_driver(self):
        """Initializes the selenium driver"""
        options = Options()
        options.headless = self.__headless
        if self.__profile_path:
            options.profile = self.__profile_path
        self.__driver = webdriver.Firefox(options=options)
        self.__driver.implicitly_wait(self.__wait_time)
        self.__driver.set_window_size(1920, 1080)
        tries = 5
        while not self.__verify_url_up(self.__schedule_url):
            if tries == 0:
                raise Exception("Hyperplanning is down")
            sleep(self.__timeout // tries)
            tries -= 1
        self.__driver.get(self.__schedule_url)
        self.__setup_schedules()
    
    def __setup_schedules(self):
        """Sets up the schedules page"""
        self.__select_section()
        self.__select_week()
        if self.__state == "F": return
        self.__select_group(1)
        self.__show_mutual_courses()

    def __show_mutual_courses(self):
        self.__driver.find_element(By.CLASS_NAME , "icon_afficher_cours_TD_plus_promo").click()
    
    def __select_section(self):
        """Selects the section on hyperplanning"""
        self.__driver.find_element(By.ID, "GInterface.Instances[1].Instances[1].bouton_Edit").click()
        self.__driver.find_element(By.ID, f"GInterface.Instances[1].Instances[1]_{self.__section_id}").click()

    def __select_group(self, group_id):
        """Selects the group on hyperplanning"""
        self.__driver.find_element(By.ID, "GInterface.Instances[1].Instances[2].bouton_Edit").click()
        self.__driver.find_element(By.ID, f"GInterface.Instances[1].Instances[2]_{group_id+1}").click()

    def __select_week(self):
        """Selects the week on hyperplanning"""
        #self.__driver.find_element(By.ID, f"GInterface.Instances[1].Instances[3]_j_{self.__week}").click()
        week = self.__driver.find_element(By.ID, f"GInterface.Instances[1].Instances[3]_j_{self.__week}")
        if week.get_attribute("innerHTML") == "F":
            self.__state = "F"
        else:
            week.click()

    def __close_driver(self):
        """Closes the selenium driver"""
        self.__driver.quit()

    @staticmethod
    def __verify_url_up(url) -> bool:
        """Checks if the page is up"""
        if head(url).status_code == 200:
            return True
        return False

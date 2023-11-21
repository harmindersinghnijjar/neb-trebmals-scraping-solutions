# Selenium 4
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

import os
import time
import pyautogui as gui


class SeleniumClass:
    def __init__(self):
        self.service = Service()
        options = webdriver.ChromeOptions()
        user = os.getlogin()
        options.add_argument(
            f"user-data-dir=C:\\Users\\{user}\\AppData\\Local\\Google\\Chrome\\User Data"
        )
        options.add_argument("--profile-directory=Default")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        self.driver = webdriver.Chrome(service=self.service, options=options)
        self.driver.get("https://chartfox.org/")
        time.sleep(5)

    def search(self, query):
        # Find the search box
        self.driver.find_element(By.CSS_SELECTOR, ".navbar-item .input").click()
        # Enter the query
        self.driver.find_element(By.CSS_SELECTOR, ".navbar-item .input").send_keys(
            query
        )
        # Find the submit button and click
        search_button = self.driver.find_element(
            By.CSS_SELECTOR, ".navbar-item:nth-child(2) .button"
        )
        search_button.click()

    def take_screenshot(self, filename):
        self.driver.save_screenshot(filename)

    def quit(self):
        self.driver.quit()


if __name__ == "__main__":
    os_command = "taskkill /im chrome.exe /f"
    os.system(os_command)
    time.sleep(5)
    selenium = SeleniumClass()
    selenium.take_screenshot("screenshot_landing_page.png")
    selenium.search("KFSO")
    selenium.take_screenshot("screenshot_panels_page.png")
    selenium.quit()
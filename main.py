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

    def get_tab_details(self):
        tab_details = self.driver.find_element(
            By.CSS_SELECTOR, "#chart-nav > div:nth-child(2) > div.tab-details"
        )
        print(tab_details.text)
        return tab_details.text


if __name__ == "__main__":
    os_command = "taskkill /im chrome.exe /f"
    os.system(os_command)
    time.sleep(5)
    selenium = SeleniumClass()
    selenium.take_screenshot("screenshot_landing_page.png")
    selenium.search("KFSO")
    selenium.take_screenshot("screenshot_panels_page.png")
    time.sleep(5)
    tabs = selenium.get_tab_details()
    # If there are tabs, then click on the first one
    if tabs:
        # Get the length of the tabs and then run a loop to click on each tab
        tab_length = len(tabs)
        print(f"Tab length: {tab_length}")
        # Loop through the tabs and click on each one
        for i in range(tab_length):
            tab = selenium.driver.find_element(
                By.CSS_SELECTOR,
                f"#chart-nav > div:nth-child(2) > div.tab-details > div:nth-child(1) > ul > li:nth-child({i+1})",
            )
            tab.click()
            time.sleep(5)
            selenium.take_screenshot(f"screenshot_tab_page_{i}.png")

    selenium.quit()

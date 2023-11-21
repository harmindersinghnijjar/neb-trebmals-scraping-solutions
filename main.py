import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os


class SeleniumClass:
    def __init__(self):
        profile = {
            "download.prompt_for_download": False,
            "download.default_directory": f"{os.getcwd()}\\downloads",
            "download.directory_upgrade": True,
            "plugins.always_open_pdf_externally": True,
        }
        options = webdriver.ChromeOptions()
        user = os.getlogin()
        options.add_argument(
            f"user-data-dir=C:\\Users\\{user}\\AppData\\Local\\Google\\Chrome\\User Data"
        )
        options.add_argument("--profile-directory=Default")
        options.add_experimental_option("prefs", profile)
        self.service = Service()
        self.driver = webdriver.Chrome(service=self.service, options=options)
        self.driver.get("https://chartfox.org/")
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".navbar-item .input"))
        )

    def search(self, query):
        search_box = self.driver.find_element(By.CSS_SELECTOR, ".navbar-item .input")
        search_box.click()
        search_box.clear()
        search_box.send_keys(query)
        search_button = self.driver.find_element(
            By.CSS_SELECTOR, ".navbar-item:nth-child(2) .button"
        )
        search_button.click()

    def take_screenshot(self, filename):
        self.driver.save_screenshot(os.path.join(os.getcwd(), filename))

    def quit(self):
        self.driver.quit()

    def get_tab_details(self):
        tab_details = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "#chart-nav > div:nth-child(2) > div.tab-details")
            )
        )
        return tab_details.text

    def highlight_element(self, element):
        self.driver.execute_script("arguments[0].style.border='3px solid red'", element)


def main():
    try:
        # Kill any existing Chrome instances to ensure a fresh start
        os_command = "taskkill /im chrome.exe /f"
        os.system(os_command)
        time.sleep(3)  # Wait a bit after killing the instances

        # Initialize the SeleniumClass instance
        selenium = SeleniumClass()

        # Take a screenshot of the landing page
        selenium.take_screenshot("screenshot_landing_page.png")

        # Search for 'KFSO'
        selenium.search("KFSO")

        # Wait for search results to load and take a screenshot
        WebDriverWait(selenium.driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "#chart-nav > div:nth-child(2) > div.tab-details")
            )
        )
        selenium.take_screenshot("screenshot_search_page.png")

        # Get tabs details
        tabs_text = selenium.get_tab_details()
        if tabs_text:
            tabs = tabs_text.split("\n")  # Assuming tabs are separated by new lines
            for i, tab in enumerate(tabs):
                # Click on the tab
                selenium.driver.find_element(
                    By.XPATH,
                    f"//div[@id='chart-nav']/div[2]/div[@class='tab-details']/div/ul/li[{i+1}]",
                ).click()

                # Highlight the tab
                selenium.highlight_element(
                    selenium.driver.find_element(
                        By.XPATH,
                        f"//div[@id='chart-nav']/div[2]/div[@class='tab-details']/div/ul/li[{i+1}]",
                    )
                )

                # Take a screenshot of the tab
                selenium.take_screenshot(f"screenshot_tab_page_{i}.png")
                # Get the chart URL
                # find all a tags
                chart_urls = selenium.driver.find_elements(By.XPATH, "//a[@href]")
                # loop through all a tags
                for chart_url in chart_urls:
                    # get the href attribute
                    href = chart_url.get_attribute("href")
                    # check if the href attribute contains .PDF
                    if href and ".PDF" in href:
                        # if it does, print it
                        print(href)
                        # Open in new tab
                        selenium.driver.execute_script(
                            f"""window.open("{href}","_blank");"""
                        )
                        # break out of the loop
                        break
        else:
            print("No tabs found")

    except Exception as e:
        print(e)

    if __name__ == "__main__":
        selenium = SeleniumClass()
def main(selenium):
    try:
        # Take a screenshot of the landing page
        selenium.take_screenshot("screenshot_landing_page.png")

        # Search for 'KFSO'
        selenium.search("KFSO")

        # Wait for search results to load and take a screenshot
        WebDriverWait(selenium.driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "#chart-nav > div:nth-child(2) > div.tab-details")
            )
        )
        selenium.take_screenshot("screenshot_search_page.png")

        # Get tabs details
        tabs_text = selenium.get_tab_details()
        if tabs_text:
            tabs = tabs_text.split("\n")  # Assuming tabs are separated by new lines
            for i, tab in enumerate(tabs):
                # Click on the tab
                selenium.driver.find_element(
                    By.XPATH,
                    f"//div[@id='chart-nav']/div[2]/div[@class='tab-details']/div/ul/li[{i+1}]",
                ).click()

                # Highlight the tab
                selenium.highlight_element(
                    selenium.driver.find_element(
                        By.XPATH,
                        f"//div[@id='chart-nav']/div[2]/div[@class='tab-details']/div/ul/li[{i+1}]",
                    )
                )

                # Take a screenshot of the tab
                selenium.take_screenshot(f"screenshot_tab_page_{i}.png")
                # Get the chart URL
                # find all a tags
                chart_urls = selenium.driver.find_elements(By.XPATH, "//a[@href]")
                # loop through all a tags
                for chart_url in chart_urls:
                    # get the href attribute
                    href = chart_url.get_attribute("href")
                    # check if the href attribute contains .PDF
                    if href and ".PDF" in href:
                        # if it does, print it
                        print(href)
                        # Download the PDF at the URL named as the tab
                        selenium.driver.get(href)
                        # Wait for the PDF to download
                        time.sleep(3)
                        # Take a screenshot of the PDF
                        selenium.take_screenshot(f"screenshot_tab_page_{i}_pdf.png")
                        # break out of the loop
                        break
        else:
            print("No tabs found")

    except Exception as e:
        print(e)


if __name__ == "__main__":
    # Kill any existing Chrome instances to ensure a fresh start
    os_command = "taskkill /im chrome.exe /f"
    os.system(os_command)
    time.sleep(3)  # Wait a bit after killing the instances

    # Initialize the SeleniumClass instance
    selenium = SeleniumClass()

    main(selenium)
    print("Done")
   
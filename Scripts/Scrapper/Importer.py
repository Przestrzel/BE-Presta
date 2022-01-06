#from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from fake_useragent import UserAgent
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pathlib import Path
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
#import cloudscraper
import time

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.maximize_window()
filePath = str(Path().absolute())+"\\courses2.csv"

def importProducts(path):
    time.sleep(1)
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "nav-sidebar")))
        nav = driver.find_element(By.ID,"nav-sidebar")

        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", nav)
        driver.find_elements(By.CSS_SELECTOR, ".material-icons.mi-settings_applications")[0].click()

        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, 'Importuj')))
            driver.find_element(By.LINK_TEXT, 'Importuj').click()

            # Choosing import category
            category = Select(driver.find_element(By.ID, 'entity'))
            category.select_by_value('1')

            file_upload = driver.find_element(By.ID,"file")

            # Choosing file to upload
            driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", file_upload)
            time.sleep(1)
            file_upload.send_keys(path)
            time.sleep(1)

            # Deleting previous products
            element = driver.find_element(By.CSS_SELECTOR,"[for='truncate_1']")
            driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", element)

            element.click()

            # Submit import
            submit_button = driver.find_element(By.NAME, "submitImportFile")

            driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", submit_button)

            submit_button.click()
            driver.switch_to.alert.accept()
            #Load configuration
            RowsToSkip = driver.find_element(By.CLASS_NAME,"fixed-width-sm")
            RowsToSkip.clear()
            RowsToSkip.send_keys('0')

            importConfig = Select(driver.find_element(By.ID,"valueImportMatchs"))
            importConfig.select_by_visible_text("basic")
            driver.find_element(By.ID,"loadImportMatchs").click()

            # import products
            driver.find_element(By.ID,"import").click()
            try:
                WebDriverWait(driver, 3600).until(EC.element_to_be_clickable((By.ID, "import_close_button")))
                close_button = driver.find_element(By.ID, "import_close_button").click()
            except:
                print("Too long import")

        except TimeoutException:
            print("Couldn't load the website")

    except TimeoutException:
        print("Couldn't load the website")

def importCsvToPresta(path):
    driver.get("http://localhost:80/admindev")
    emailbox = driver.find_element(By.ID,"email")
    emailbox.clear()
    emailbox.send_keys("admin@admin.com")
    passwordbox = driver.find_element(By.ID,"passwd")
    passwordbox.clear()
    passwordbox.send_keys("admin123")
    passwordbox.send_keys(Keys.RETURN)

    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID,"subtab-AdminImport")))
        # Import files
        importProducts(filePath)

    except TimeoutException:
        print("Couldn't load the website")

importCsvToPresta(filePath)
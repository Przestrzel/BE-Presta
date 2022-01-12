import re
from time import sleep
from random import randint
from selenium import webdriver
from pathlib import Path
from selenium.webdriver.common.by import By

PATH = str(Path().absolute())+"\\chromedriver.exe"
chromeDriver = webdriver.Chrome(PATH)
chromeDriver.maximize_window()
basicURL = "https://localhost:2589/index.php?"

class shoppingTest:
    def __init__(self):
        self.__categories = ["id_category=11&controller=category", "id_category=10&controller=category"]
        self.__makeAll()

    def __makeAll(self):
        self.__addingElements()
        self.__goToURL("controller=cart&action=show")
        sleep(1)
        self.__deleteElement()
        sleep(2)
        self.__goToURL("controller=order")
        self.__createAccount()
        self.__makeAdress()
        self.__deliveryOption()
        self.__paymentOption()
        self.__checkStatus()


    def __addingElements(self):
        for _ in range(10):
            i = randint(0, len(self.__categories)-1)
            self.__goToURL(self.__categories[i] + "&page?=" + str(randint(0, 5)))
            self.__addElement(randint(1, 4), randint(0, 11))  # losowanie liczby elementów, lososwanie numeru


    def __addElement(self, counter, productNo):
        product = chromeDriver.find_elements(By.CSS_SELECTOR, ".product-title > a")[productNo]
        chromeDriver.get(product.get_attribute("href"))
        counter_button = chromeDriver.find_elements(By.CSS_SELECTOR, ".btn.btn-touchspin.js-touchspin.bootstrap-touchspin-up")[0]
        for _ in range(counter-1):
            counter_button.click()
        sleep(2)

        chromeDriver.find_elements(By.CSS_SELECTOR, ".product-actions .add-to-cart")[0].click()
        sleep(1)
        #chromeDriver.find_element(By.CSS_SELECTOR, ".cart-content-btn button").click()
        self.__pageLoaded()

    def __goToURL(self, name):
        chromeDriver.get(basicURL + name)
        self.__pageLoaded()

    def __pageLoaded(self):
        page = chromeDriver.execute_script('return document.readyState;')
        return page == 'complete'

    def __deleteElement(self):
        elements = chromeDriver.find_elements(By.CLASS_NAME, "remove-from-cart")
        sleep(1)
        elements[randint(0, len(elements))].click()
        sleep(1)
        self.__pageLoaded()

    def __createAccount(self):
        chromeDriver.find_elements(By.CSS_SELECTOR, ".radio-inline")[1].click()
        chromeDriver.find_element(By.CSS_SELECTOR, "input[name=firstname]").send_keys("Anna")
        chromeDriver.find_element(By.CSS_SELECTOR, "input[name=lastname]").send_keys("Kowalska")
        chromeDriver.find_element(By.CSS_SELECTOR, "input[name=email]").send_keys("anna."+str(randint(0, 100))+"kowalska"+str(randint(0,40))+"@example.com")
        chromeDriver.find_element(By.CSS_SELECTOR, "input[name=password]").send_keys("qwerty")
        buttoms = chromeDriver.find_elements(By.CSS_SELECTOR, ".custom-checkbox")
        for buttom in buttoms:
            buttom.click()
        chromeDriver.find_element(By.CSS_SELECTOR, '.continue').click()
        sleep(0.5)

    def __makeAdress(self):
        chromeDriver.find_element(By.CSS_SELECTOR, "input[name=address1]").send_keys("ulica 1")
        chromeDriver.find_element(By.CSS_SELECTOR, "input[name=postcode]").send_keys("12-121")
        chromeDriver.find_element(By.CSS_SELECTOR, "input[name=city]").send_keys("miasto")
        chromeDriver.find_element(By.CSS_SELECTOR, "button[name='confirm-addresses']").click()

    def __deliveryOption(self):
        sleep(0.5)
        chromeDriver.find_element(By.ID, "delivery_option_10").click()
        sleep(1)
        chromeDriver.find_element(By.NAME, "confirmDeliveryOption").click()

    def __paymentOption(self):
        chromeDriver.find_element(By.ID, "payment-option-2").click()
        chromeDriver.find_element(By.ID, "conditions_to_approve[terms-and-conditions]").click()
        sleep(1)
        chromeDriver.find_element(By.CSS_SELECTOR, "#payment-confirmation button").click()

    def __checkStatus(self):
        self.__goToURL("controller=my-account")
        chromeDriver.find_element(By.ID, "history-link").click()
        sleep(0.5)
        chromeDriver.find_elements(By.CSS_SELECTOR, ".page-customer-account #content .order-actions a")[0].click()


x = shoppingTest()
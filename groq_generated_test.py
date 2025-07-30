from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.username_input = (By.ID, "user-name")
        self.password_input = (By.ID, "password")
        self.login_button = (By.ID, "login-button")

    def enter_username(self, username):
        self.driver.find_element(*self.username_input).send_keys(username)

    def enter_password(self, password):
        self.driver.find_element(*self.password_input).send_keys(password)

    def click_login(self):
        self.driver.find_element(*self.login_button).click()

class ProductsPage:
    def __init__(self, driver):
        self.driver = driver
        self.shopping_cart_container = (By.CSS_SELECTOR, ".shopping_cart_container")
        self.inventory_items = (By.CSS_SELECTOR, ".inventory_item")

    def wait_for_login(self):
        WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(self.shopping_cart_container))

    def get_inventory_items(self):
        items = self.driver.find_elements(*self.inventory_items)
        item_names = [item.find_element(By.CSS_SELECTOR, ".inventory_item_name").text for item in items]
        item_prices = [item.find_element(By.CSS_SELECTOR, ".inventory_item_price").text for item in items]
        return list(zip(item_names, item_prices))

class TestSauceDemoLogin:
    def test_login(self):
        options = Options()
        options.headless = False
        driver = webdriver.Chrome(options=options)
        driver.get("https://www.saucedemo.com/")

        login_page = LoginPage(driver)
        login_page.enter_username("standard_user")
        login_page.enter_password("secret_sauce")
        login_page.click_login()

        products_page = ProductsPage(driver)
        products_page.wait_for_login()

        inventory_items = products_page.get_inventory_items()
        for item in inventory_items:
            print(f"Item: {item[0]}, Price: {item[1]}")

        driver.quit()

if __name__ == "__main__":
    test = TestSauceDemoLogin()
    test.test_login()
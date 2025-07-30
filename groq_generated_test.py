from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Set up Chrome WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)

# Navigate to Amazon UK
driver.get("https://www.amazon.co.uk/")

# Find and click the sign in button
sign_in_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "nav-link-accountList"))
)
sign_in_button.click()

# Find and click the email signin button
driver.get("https://www.amazon.co.uk/ap/signin?_encoding=UTF8&ignoreAuthState=1")

# Find and enter email
email_input = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.ID, "ap_email"))
)
email_input.send_keys("your_email@example.com")

# Find and enter password
password_input = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.ID, "ap_password"))
)
password_input.send_keys("your_password")

# Find and click the login button
login_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "signInSubmit"))
)
login_button.click()

# Verify we are on the dashboard page
try:
    WebDriverWait(driver, 10).until(
        EC.title_contains("Amazon")
    )
    print("Login successful. We are on the dashboard page.")
except TimeoutException:
    print("Login failed. We are not on the dashboard page.")

# Close the browser
driver.quit()
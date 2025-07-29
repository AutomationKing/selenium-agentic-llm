# Task: Open Chrome and go to https://www.asda.jobs/

# Write a simple code using Selenium that:
# - Opens Chrome
# - Navigates to a website
# - Waits 5 seconds
# - Closes the browser

from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Start your code below:

# Open the browser
driver = webdriver.Chrome()

# Navigate to the website
driver.get("https://www.asda.jobs/")

# Wait 5 seconds
time.sleep(5)

# Close the browser
driver.close()

# End your code

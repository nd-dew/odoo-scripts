from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from time import sleep
from faker import Faker
fake = Faker()
NAME  = fake.name()
EMAIL = f'{NAME.replace(" ", "")}@gmail.com'

MILISECOND_DELAY_BETWEEN_STEPS=10 #ms

def wait(t=1):
    sleep(t*0.001*MILISECOND_DELAY_BETWEEN_STEPS)

# Set up Chrome options
options = Options()
# options.add_argument("--headless")  # Run Chrome in headless mode
options.add_experimental_option('detach', True)
options.add_argument("--window-size=800,1400")
options.add_argument("--force-device-scale-factor=0.2")
service = Service(executable_path="/usr/lib/chromium-browser/chromedriver")
driver = webdriver.Chrome(service=service, options=options)

# URL to open
url = "http://localhost:8069/shop"

# Open the URL
driver.get(url)

# Optionally, you can print the page title to verify if the URL opened successfully
print("Page Title:", driver.title, "click on first item")

first_shoppable_item = driver.find_element(By.CSS_SELECTOR, ".oe_product_image_link")
first_shoppable_item.click()

add_to_cart_btn = driver.find_element(By.CSS_SELECTOR, "#add_to_cart_wrap")
add_to_cart_btn.click()

wait(200)
checkout_btn = driver.find_element(By.XPATH, '//*[contains(text(), "Checkout")]')
checkout_btn.click()

wait(200)
pay_with_demo_btn = driver.find_element(By.XPATH, '//*[contains(text(), "Demo")]')
pay_with_demo_btn.click()

wait(200)
pay_btn = driver.find_element(By.CSS_SELECTOR, "button[name=o_payment_submit_button]")
pay_btn.click()
wait(200)

# Close the browser
# driver.quit()

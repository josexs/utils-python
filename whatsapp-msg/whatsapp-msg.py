from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

chromepath = "PATH" # Path chromedriver
target = "NAME" # name of contact or group
msg = "vamos ninio2" # msg

try:
    options = webdriver.ChromeOptions()
    options.add_argument('--user-data-dir=/Users/jgomepav/bin/chromeDriverData')
    driver = webdriver.Chrome(
        executable_path=chromepath, chrome_options=options)

    driver.get("https://web.whatsapp.com/")
    driver.minimize_window()
    wait = WebDriverWait(driver, 600)

    x_arg = '//span[contains(@title,"' + target + '")]'
    group_title = wait.until(EC.presence_of_element_located((
        By.XPATH, x_arg)))
    group_title.click()

    inp_xpath = '//p[contains(@class, "selectable-text copyable-text")]'
    input_box = wait.until(EC.presence_of_element_located((
        By.XPATH, inp_xpath)))
    for i in range(100):
        input_box.send_keys(msg + Keys.ENTER)
        time.sleep(1)
except ValueError:
    print('Error')
finally:
    driver.quit()

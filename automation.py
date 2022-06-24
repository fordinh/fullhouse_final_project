import os.path
import random
import time

from selenium import webdriver
from selenium.webdriver import Chrome as Driver, Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


def get_crx_file():
    return [f.path for f in os.scandir('config\\crxs') if f.is_file()]


def generate_driver():
    options = Options()
    extensions = get_crx_file()
    for extension in extensions:
        options.add_extension(extension)

    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    ser = Service("config\\chromedriver.exe")
    driver = webdriver.Chrome(service=ser, options=options)
    time.sleep(5)
    windows = len(driver.window_handles)
    if windows > 1:
        for i in range(windows - 1):
            driver.switch_to.window(driver.window_handles[0])
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(0.5)

    return driver


def click(driver, xpath, enter=False, send_key=None, sleep=0.0, wait_element_is_visible=2, random_click=False,
          ctrl_enter=False, clear=True):
    try:
        if wait_element_is_visible > 0:
            while True:
                element = driver.find_elements(By.XPATH, xpath)
                if len(element) != 0:
                    break
                print(f'wait until complete xpath = {xpath}')
                time.sleep(wait_element_is_visible)
        else:
            element = driver.find_elements(By.XPATH, xpath)

        if len(element) > 0:
            if not random_click:
                driver.execute_script("arguments[0].click();", element[0])

            if not send_key:
                time.sleep(sleep)

            else:
                time.sleep(1)
                if clear:
                    element[0].clear()
                # element[0].send_keys(send_key)
                for i in send_key:
                    element[0].send_keys(i)
                    time.sleep(float(random.randint(20, 100) / 1000))
                if enter:
                    element[0].send_keys(Keys.ENTER)
                    time.sleep(sleep)

                if ctrl_enter:
                    element[0].send_keys(Keys.CONTROL + Keys.RETURN)
                    time.sleep(sleep)

                time.sleep(2)

    except Exception as e:
        print(f'Lỗi ở click XPATH = {xpath}')
        print(e)

    return driver


def scroll_and_click_by_xpath(
        driver, xpath, delta=4,
        is_click=True, is_scroll=True,
        text=None, enter=False, sleep=0.0
):
    elements = driver.find_elements(By.XPATH, xpath)
    if len(elements) == 0:
        return driver, False

    if is_scroll:
        position = elements[0].rect
        time.sleep(1)
        current_offset = driver.execute_script("return window.pageYOffset")
        range_scroll = int((position['y'] - current_offset) / 50)

        i = 0
        if range_scroll > 0:
            while i < range_scroll - delta:
                delta_scroll = random.randint(2, delta)
                driver.execute_script("window.scrollBy({top: " + str(delta_scroll * 50) + ", behavior: 'smooth'});")
                i += delta_scroll

                time.sleep(float(random.randint(800, 1200) / 1000))
        else:
            while i < abs(range_scroll) + delta:
                delta_scroll = random.randint(2, delta)
                driver.execute_script(
                    "window.scrollBy({top: " + str(delta_scroll * (-1) * 50) + ", behavior: 'smooth'});")
                i += delta_scroll

                time.sleep(float(random.randint(800, 1200) / 1000))

    if is_click:
        driver = click(driver, xpath, send_key=text, sleep=sleep, enter=enter)

    return driver, True

# def download(driver, xpath):
#     link = driver.find_elements_by_xpath(xpath).get_attribute("href")
#     print(link)

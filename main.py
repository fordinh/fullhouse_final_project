import time
import requests
from automation import *
import os

session = requests.Session()


# def next_page(driver):
#     list_page = []
#     pages = driver.find_elements(By.XPATH, '//div[@class="paginations mrt-30"]//a')
#     for page in pages:
#         url = page.get_property('href')
#         list_page.append(url)
#         print(len(list_page), list_page)
#     return driver, list_page


def find_product(driver):
    list_links = []
    for index in range(1, 5):
        driver.get(f'https://loza.vn/categories/storefront?&page={index}')
        time.sleep(5)
        links = driver.find_elements(By.XPATH, '//div[@class="img-template-dnt"]//a')
        for link in links:
            url = link.get_property('href')
            list_links.append(url)
    print(len(list_links), list_links)
    return driver, list_links


def get_img_url(driver):
    driver, list_links = find_product(driver)
    for index, link in enumerate(list_links):
        driver.get(link)
        time.sleep(5)
        list_url = []
        images = driver.find_elements(By.XPATH, '(//img[@class="img-slide-dnt-zoom"])')
        for image in images:
            url = image.get_property('src')
            list_url.append(url)
        folder_name = link.split("/")[-1]

        if not os.path.exists(f'img/{folder_name}'):
            os.makedirs(f'img/{folder_name}')
        save_img(list_url, folder_name)


def save_img(list_url, folder_name):
    for index, url in enumerate(list_url):
        try:
            response = session.get(url)
            with open(f'img/{folder_name}/product_{index}.jpg', 'wb') as f:
                f.write(response.content)
                f.close()

            print(f'Đã lưu ảnh img/{folder_name}/product_{index}.jpg')
        except Exception as e:
            print(e)


driver = generate_driver()
driver = get_img_url(driver)

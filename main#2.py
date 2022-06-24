import time
import requests
from automation import *
import os
import concurrent
from concurrent.futures import ThreadPoolExecutor

session = requests.Session()


def send_with_thread_executor(max_workers, jobs):
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for job in jobs:
            futures.append(
                    executor.submit(
                        save_img, job[0], job[1]
                    )
                )


def find_product(driver):
    list_links = []
    for index in range(1, 2):
        driver.get(f'https://loza.vn/categories/storefront?&page={index}')
        time.sleep(5)
        links = driver.find_elements(By.XPATH, '//div[@class="img-template-dnt"]//a')
        for link in links:
            url = link.get_property('href')
            list_links.append(url)
            print(f'Đang ở url này: {url}')
    print(len(list_links), list_links)
    return driver, list_links


def get_img_url(driver):
    final_results = []
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
        # save_img(list_url, folder_name)
        final_results.append([list_url.copy(), folder_name])

    send_with_thread_executor(5, jobs=final_results)


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

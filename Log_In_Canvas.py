from automation import *
import time
driver = generate_driver()
driver.get("https://courses.mizzouk12.missouri.edu/login/canvas")
time.sleep(5)
driver = click(driver, '//input[@id="pseudonym_session_unique_id"]', send_key='dinhquoc2004@gmail.com')
driver = click(driver, '//input[@id="pseudonym_session_password"]', send_key='asdfasdf', enter=True)
time.sleep(1000)
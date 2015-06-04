
from selenium import webdriver
import time


driver = webdriver.Firefox()
driver.get('http://0.0.0.0:5000/input_custom_data')
element = driver.find_element_by_name('input_data')
element.send_keys('sin(x)*cos(x)')  # input function
element = driver.find_element_by_name('first_border')
element.send_keys(3)  # input first border
element = driver.find_element_by_name('second_border')
element.send_keys(1000)  # input second border
element = driver.find_element_by_name('slice')
element.send_keys(500)  # input n
element = driver.find_element_by_id('send')
element.click()
driver.get('http://0.0.0.0:5000/')
element = driver.find_element_by_id('calculate')
element.click()
time.sleep(7)
elem = driver.find_element_by_id('result_worker')
print elem.text
driver.close()





import pytest
from selenium import webdriver
import random
from selenium.webdriver.support.ui import Select
import time


link = 'http://localhost/litecart/en/create_account'

random_number = random.randint(10000, 90000)
first_name = f'TestFirstName{random_number}'
last_name = f'TestLastName{random_number}'
address_1 = f'Lenina{random_number}'
postcode = random_number
city = f'TestCity{random_number}'
country = 'United States'
email = f'test_{random_number}@mail.com'
phone_number = f'+1{random_number}'
password = random_number


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    request.addfinalizer(wd.quit)
    return wd


def test_for_lesson(driver):
    driver.get(link)
    driver.implicitly_wait(10)
    select = Select(driver.find_element_by_xpath("//select[@name = 'country_code']"))
    select.select_by_visible_text('United States')

    driver.find_element_by_xpath("//input[@name='firstname']").send_keys(first_name)
    driver.find_element_by_xpath("//input[@name='lastname']").send_keys(last_name)
    driver.find_element_by_xpath("//input[@name='address1']").send_keys(address_1)
    driver.find_element_by_xpath("//input[@name='postcode']").send_keys(postcode)
    driver.find_element_by_xpath("//input[@name='city']").send_keys(city)
    driver.find_element_by_xpath("//input[@name='email']").send_keys(email)
    driver.find_element_by_xpath("//input[@name='phone']").send_keys(phone_number)
    driver.find_element_by_xpath("//input[@name='password']").send_keys(password)
    driver.find_element_by_xpath("//input[@name='confirmed_password']").send_keys(password)
    driver.find_element_by_xpath("//button[@name='create_account']").click()

    driver.find_element_by_xpath("//a[text()='Logout']").click()

    driver.find_element_by_xpath("//input[@name='email']").send_keys(email)
    driver.find_element_by_xpath("//input[@name='password']").send_keys(password)
    driver.find_element_by_xpath("//button[@name='login']").click()
    driver.find_element_by_xpath("//a[@href='http://localhost/litecart/en/logout']").click()

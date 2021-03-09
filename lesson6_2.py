import datetime
import pytest
from selenium import webdriver
import time
import os
from datetime import date
from selenium.webdriver.support.ui import Select

link = 'http://localhost/litecart/admin/login.php'
login = 'admin'
password = 'admin'
test_name_product = 'Test_Product'

@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    request.addfinalizer(wd.quit)
    return wd


def test_for_lesson(driver):
    driver.implicitly_wait(5)
    driver.get(link)
    driver.find_element_by_name("username").send_keys(login)
    driver.find_element_by_name("password").send_keys(password)
    driver.find_element_by_name("login").click()
    time.sleep(1)
    driver.find_element_by_xpath("//span[text()='Catalog']").click()
    time.sleep(1)
    driver.find_element_by_css_selector("#content > div:nth-child(2) > a:nth-child(2)").click()
    time.sleep(1)


    #  Заполнение полей на вкладке General
    driver.find_element_by_xpath("//input [@type='radio' and @value ='1']").click()
    driver.find_element_by_xpath("//input [@type='text' and @name='name[en]']").send_keys(test_name_product)
    driver.find_element_by_xpath("//input[@name='code']").send_keys("777")
    driver.find_element_by_xpath("//input[@name='product_groups[]' and @value='1-2' ]").click()
    Quantity = driver.find_element_by_xpath("//input[@name='quantity']")
    Quantity.clear()
    Quantity.send_keys('1')

    current_dir = os.path.abspath(os.path.dirname(__file__))  # получаем путь к директории текущего исполняемого файла
    file_path = os.path.join(current_dir, 'ufo-clipart-alien-ship-498126.png')  # добавляем к этому пути имя файла
    download_file = driver.find_element_by_xpath("//input[@type='file']")
    download_file.send_keys(file_path)

    current_date = date.today()
    future_date = current_date + datetime.timedelta(days=5)
    date_valid_from = driver.find_element_by_xpath("//input[@name='date_valid_from']")
    date_valid_from.send_keys(current_date.strftime('%d%m%Y'))
    date_valid_to = driver.find_element_by_xpath("//input[@name='date_valid_to']")
    date_valid_to.send_keys(future_date.strftime('%d%m%Y'))

    driver.find_element_by_xpath("//a[@href='#tab-information']").click()
    time.sleep(2)

    select = Select(driver.find_element_by_xpath("//select[@name='manufacturer_id']"))
    select.select_by_visible_text('ACME Corp.')

    keywords = driver.find_element_by_xpath("//input[@name='keywords']")
    keywords.send_keys("Test")
    short_description = driver.find_element_by_xpath("//input[@name='short_description[en]']")
    short_description.send_keys("Test_short_description")
    trumbowyg_editor = driver.find_element_by_css_selector("div.trumbowyg-editor")
    trumbowyg_editor.send_keys("Test")
    driver.find_element_by_xpath("//input[@name='head_title[en]']").send_keys('Head_test_title')
    driver.find_element_by_xpath("//input[@name='meta_description[en]']").send_keys('Meta_test_description')

    driver.find_element_by_xpath("//a[@href='#tab-prices']").click()
    time.sleep(2)
    price = driver.find_element_by_xpath("//input[@name='purchase_price']")
    price.clear()
    price.send_keys('100')
    driver.find_element_by_xpath("//button[@name='save']").click()

    time.sleep(2)
    name_product = driver.find_element_by_css_selector('tr:nth-child(4) > td:nth-child(3) > a')

    assert name_product.text == test_name_product


import time

import pytest
from selenium import webdriver


link_test_1 = 'http://localhost/litecart/admin/?app=countries&doc=countries'
link_test_2 = "http://localhost/litecart/admin/?app=geo_zones&doc=geo_zones"
login = 'admin'
password = 'admin'


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    request.addfinalizer(wd.quit)
    return wd


def test_1_a(driver):
    # 1) на    странице http: // localhost / litecart / admin /?app = countries & doc = countries
    # а) проверить, что страны расположены в алфавитном порядке
    driver.get(link_test_1)
    driver.find_element_by_name("username").send_keys(login)
    driver.find_element_by_name("password").send_keys(password)
    driver.find_element_by_name("login").click()

    countries_list = driver.find_elements_by_css_selector('tr.row')
    name_countries = []

    for countries in countries_list:
        name = countries.find_element_by_css_selector("td:nth-child(5)").text
        name_countries.append(name)

    assert name_countries == sorted(name_countries)


def test_1_b(driver):
    # б) для тех стран, у которых количество зон отлично от нуля -- открыть страницу этой страны и там проверить,
    # что зоны расположены в алфавитном порядке
    driver.get(link_test_1)
    driver.find_element_by_name("username").send_keys(login)
    driver.find_element_by_name("password").send_keys(password)
    driver.find_element_by_name("login").click()

    countries_list = driver.find_elements_by_css_selector('tr.row')
    link_zone = []  # Список для адресов

    for countries in countries_list:
        zone = countries.find_element_by_css_selector("td:nth-child(6)").text
        if int(zone) > 0:  # Если количество зон > 0, выдёргиваем ссылку на зону и сохраняем в список
            link_in = countries.find_element_by_css_selector("td:nth-child(5) > a").get_attribute("href")
            link_zone.append(link_in)

    for zone in link_zone:  # Проходим по всем ссылкам в списке
        driver.get(zone)
        country_name = driver.find_elements_by_xpath('//input[@type="hidden"][contains (@name, "[name]")]')  #
        # Получаем список обьектов в таблице

        country_name_two = []
        for country in country_name:
            country_name_two.append(country.get_attribute("value"))
        assert country_name_two == sorted(country_name_two)
        driver.back()


def test_2(driver):
    # 2) на странице http: // localhost / litecart / admin /?app = geo_zones & doc = geo_zones зайти в каждую из
    # стран и проверить, что зоны расположены в алфавитном порядке
    driver.get(link_test_2)
    driver.find_element_by_name("username").send_keys(login)
    driver.find_element_by_name("password").send_keys(password)
    driver.find_element_by_name("login").click()
    edit_elements_list = driver.find_elements_by_xpath("//a[@title='Edit']")
    count = 0
    link_l = [link.get_attribute('href') for link in edit_elements_list]


    while count < len(link_l):
        driver.get(link_l[count])
        # time.sleep(2)  # Без задержки падает тест, даже с использованием ожидания
        zone_names = driver.find_elements_by_xpath('//select[contains (@name, "zone_code")]//option[@selected="selected"]')
        list_assert = []
        for name in zone_names:
            list_assert.append(name.get_attribute('text'))
        assert list_assert == sorted(list_assert)
        count += 1
        driver.back()




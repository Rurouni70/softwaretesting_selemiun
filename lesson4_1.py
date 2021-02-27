import pytest
from selenium import webdriver

link = 'http://localhost/litecart/admin/login.php'
login = 'admin'
password = 'admin'


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    request.addfinalizer(wd.quit)
    return wd


def test_for_lesson(driver):
    driver.get(link)
    driver.find_element_by_name("username").send_keys(login)
    driver.find_element_by_name("password").send_keys(password)
    driver.find_element_by_name("login").click()

    count_menu_elements = len(driver.find_elements_by_id("app-"))
    num = 0

    while num < count_menu_elements:
        new_element_menu = driver.find_elements_by_id("app-")
        new_element_menu[num].click()
        sub_menu_list = driver.find_elements_by_css_selector('#app- ul li')
        if len(sub_menu_list) > 0:
            sub_menu_count = 0
            while sub_menu_count < len(sub_menu_list):
                element_sub_menu = driver.find_elements_by_css_selector('#app- ul li')
                element_sub_menu[sub_menu_count].click()
                h1 = driver.find_elements_by_css_selector('#content > h1')
                assert len(h1) == 1
                sub_menu_count += 1
        num += 1

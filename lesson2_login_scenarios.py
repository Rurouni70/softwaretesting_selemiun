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

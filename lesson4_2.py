import pytest
from selenium import webdriver

link = 'http://localhost/litecart/en/'
login = 'admin'
password = 'admin'

@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    request.addfinalizer(wd.quit)
    return wd


# div.content > ul > li.product
# div.image-wrapper > div

def test_for_lesson(driver):
    driver.get(link)

    all_elements_list = driver.find_elements_by_css_selector("div.content > ul > li.product")

    for element in all_elements_list:
        sticker = element.find_elements_by_css_selector("div.image-wrapper > div")
        assert len(sticker) == 1


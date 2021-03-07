import re

import pytest
from selenium import webdriver

link_test = 'http://localhost/litecart/en/'


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    request.addfinalizer(wd.quit)
    return wd


def test_1_a(driver):
    driver.get(link_test)
    driver.implicitly_wait(3)

    duck = driver.find_element_by_css_selector('#box-campaigns li.product')
    name_duck_in_main_page = driver.find_element_by_css_selector('#box-campaigns div.name').text
    regular_price_in_main_page = driver.find_element_by_css_selector('#box-campaigns s.regular-price')
    regular_price_m = regular_price_in_main_page.text
    sale_price_in_main_page = driver.find_element_by_css_selector('#box-campaigns strong')

    regular_price_color_main_page = regular_price_in_main_page.value_of_css_property('color')
    regular_through_price = regular_price_in_main_page.value_of_css_property('text-decoration')  # return "line-through solid rgb(119, 119, 119)"
    regular_size_font_main = float(regular_price_in_main_page.value_of_css_property('font-size').replace('px', ''))

    sale_price_color_in_mane_page = sale_price_in_main_page.value_of_css_property('color')
    sale_price_m = sale_price_in_main_page.text
    sale_price_bold_in_main_page = sale_price_in_main_page.value_of_css_property('font-weight')  # return "700"
    sale_price_font_size_main_page = float(sale_price_in_main_page.value_of_css_property('font-size').replace('px', ''))

    duck.click()

    name_duck_in_product_page = driver.find_element_by_css_selector('h1.title').get_attribute('textContent')
    regular_price_in_product_page = driver.find_element_by_css_selector('div s.regular-price')
    regular_price_p = regular_price_in_product_page.text
    sale_price_in_product_page = driver.find_element_by_css_selector('strong.campaign-price')
    sale_price_p = sale_price_in_product_page.text
    regular_price_color_product_page = regular_price_in_product_page.value_of_css_property('color')
    regular_through_price_product = regular_price_in_product_page.value_of_css_property('text-decoration')  # return "line-through solid rgb(119, 119, 119)

    sale_price_bold_in_product_page = sale_price_in_product_page.value_of_css_property('font-weight')  # return "700"
    sale_price_color_in_product_page = sale_price_in_product_page.value_of_css_property('color')

    sale_price_font_size_product_page = float(sale_price_in_product_page.value_of_css_property('font-size').replace('px', ''))
    regular_price_font_size_product_page = float(regular_price_in_product_page.value_of_css_property('font-size').replace('px', ''))


    def get_rgb_color(element_color_property):
        """ Функция для обработки свойства цвет у элемента. Возвращает список с кодами цвета RGBa """
        rgb_color = re.findall(r'\d+', element_color_property)
        return rgb_color

    def is_gray(rgb_color):
        """" Функция для проверки, является ли цвет серым """
        if rgb_color[0] == rgb_color[1] == rgb_color[2]:
            return True
        else:
            return False

    def is_red(rgb_color):
        """" Функция для проверки, является ли цвет серым """
        if int(rgb_color[1]) == 0 and int(rgb_color[2]) == 0:
            return True
        else:
            return False

    def text_height_comparison(regular_price, sale_price):
        """"Функиця для сравнения высоты текста акционной и обычной цены"""
        if sale_price > regular_price:
            return True
        else:
            return False


    # а) на главной странице и на странице товара совпадает текст названия товара
    assert name_duck_in_main_page == name_duck_in_product_page

    #  б) на главной странице и на странице товара совпадают цены (обычная и акционная)
    assert regular_price_m == regular_price_p
    assert sale_price_p == sale_price_m

    # обычная цена серая на главной странице магазина
    assert is_gray(get_rgb_color(regular_price_color_main_page))
    # обычная цена серая на странице товара
    assert is_gray(get_rgb_color(regular_price_color_product_page))

    # обычная цена зачёркнутая на главной странице

    # обычная цена зачёркнутая на странице товара

    # акционная цена жирная на главной странице
    # акционная цена жирная на странице товара

    # акционная цена красная на главной странице
    assert is_red(get_rgb_color(sale_price_color_in_mane_page))
    # акционная цена красная на странице товара
    assert is_red(get_rgb_color(sale_price_color_in_product_page))

    # д) акционная цена крупнее, чем обычная на главное странице
    assert text_height_comparison(regular_size_font_main, sale_price_font_size_main_page)
    # д) акционная цена крупнее, чем обычная на странице продукта
    assert text_height_comparison(regular_price_font_size_product_page, sale_price_font_size_product_page)

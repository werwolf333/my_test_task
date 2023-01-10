import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common import NoSuchElementException
from selenium.webdriver import ActionChains
import re
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


def set_selenium_range(start, end):
    args_XPATH = {}
    args_XPATH['name_app'] = [
        '//*[@id="main"]/div/div/div[1]/div[1]/div[1]/div/h1',
        '//*[@id="main"]/div/div/div[1]/div[2]/div[1]/div/h1',
    ]
    args_XPATH['name_company'] = [
        '//*[@id="main"]/div/div/div[1]/div[2]/div[1]/div[2]/div[5]/div/div[2]/a',
        '//*[@id="main"]/div/div/div[1]/div[2]/div[1]/div/a'
    ]
    args_XPATH['release_year'] = [
        '//*[@id="main"]/div/div/div[1]/div[3]/div[1]/div[2]/div[5]/div/div[1]/span/div/span',
        '//*[@id="main"]/div/div/div[1]/div[3]/div[1]/div[2]/div[6]/div/div[1]/span/div/span',
        '//*[@id="main"]/div/div/div[1]/div[3]/div[1]/div[2]/div[7]/div/div[1]/span/div/span',
        '//*[@id="main"]/div/div/div[1]/div[3]/div[1]/div[2]/div[4]/div/div[1]/span/div/span',
        '//*[@id="main"]/div/div/div[1]/div[3]/div[1]/div[2]/div[6]/div/div[1]/span/div/span',
        '//*[@id="main"]/div/div/div[2]/div[3]/div[1]/div[2]/div[6]/div/div[1]/span/div/span',
    ]

    args_XPATH['mail'] = [
        '//*[@id="main"]/div/div/div[1]/div[2]/div[1]/div[2]/div[1]/pre',
        '//*[@id="main"]/div/div/div[1]/div[3]/div[1]/div[2]/div[1]/pre'
    ]

    driver = webdriver.Chrome()
    start_way_XPATH = '//*[@id="all-products-listall-list-container"]/div/div'
    for num in range(start, end):
        driver.get("https://apps.microsoft.com/store/category/Business")
        way = start_way_XPATH + '[' + str(num) + ']'
        time.sleep(2)
        reg_find = True
        while reg_find:
            try:
                time.sleep(0.5)
                elem = driver.find_element(By.XPATH, way)
                if elem.is_displayed():
                    reg_find = False
                else:
                    ActionChains(driver).scroll_by_amount(0, 600).perform()
            except NoSuchElementException:
                time.sleep(0.5)
                ActionChains(driver).scroll_by_amount(0, 900).perform()

        elem.click()
        time.sleep(2)
        yield (find_info(args_XPATH, driver))


def get_elem(options, driver):
    elem = None
    for option in options:
        if (elem == None):
            try:
                elem = WebDriverWait(driver.find_element(By.XPATH, option), 20).until(
                    EC.presence_of_element_located((By.XPATH, option)))
            except NoSuchElementException:
                elem = None
    return elem


def find_name_and_company(options, driver, key):
    args = {}
    elem = get_elem(options, driver)
    if (elem != None):
        args[key] = elem.text
    else:
        args[key] = elem
    return args


def find_year(options, driver, key):
    args = {}
    elem = get_elem(options, driver)
    if (elem != None):
        args[key] = elem.text[-5:]
    else:
        args[key] = elem
    return args

def find_mail(options, driver, key):
    args = {}
    elem = get_elem(options, driver)
    if(elem!=None):
        result = re.search(r"[-\w\.]+@([-\w]+\.)+[-\w]{2,4}", elem.text)
    else:
        result = None
    if(result != None):
        args[key] = result.group(0)
    else:
        args[key] = result
    return args


def find_info(args_XPATH, driver):
    info = {}
    for key, options in args_XPATH.items():
        if (key == 'mail'):
            mail = find_mail(options, driver, key)
            info = {**info, **mail}
        elif(key =='release_year'):
            year = find_year(options, driver, key)
            info = {**info, **year}
        else:
            no_mail = find_name_and_company(options, driver, key)
            info = {**info, **no_mail}
    return info

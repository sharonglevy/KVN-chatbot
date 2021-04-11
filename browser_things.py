# -*- coding: utf-8 -*-
"""
Created on Mon Aug 26 15:37:48 2019

@author: agustin.mediavilla
"""
from selenium.webdriver.common.keys import Keys
from selenium import (webdriver)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains as Actions
from selenium.webdriver.remote import errorhandler as err
from selenium.common import exceptions as exp

import time
from selenium_room_reservation import config
import psutil



def kill_task(process_name):
    for proc in psutil.process_iter():
        # check whether the process name matches
        if proc.name() == process_name:
            proc.kill()


def start_browser():
    try:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument(r"user-data-dir=C:\\Users\\"+config.user_data["eid"]+"\\Desktop\\Keep It Simple\\Python\\Profile 1")
        #wd = webdriver.Chrome(executable_path=r"C:\\Users\\"+config.user_data["eid"]+"\\Desktop\\Keep It Simple\\Python\\chromedriver.exe", options=chrome_options)
        wd = webdriver.Chrome(executable_path=r"C:\\Users\\sharon.gabriela.levy\\Downloads\\chromedriver_win32\\chromedriver.exe", options=chrome_options)
        wd.implicitly_wait(5)
    except:
        kill_task("chrome.exe")
        kill_task("chromedriver.exe")
        wd = start_browser()
    return wd


def initialize():
    kill_task("chrome.exe")
    kill_task("chromedriver.exe")
    global driver
    driver = start_browser()


def login_sso():
    logbox = wait_element_id("formsAuthenticationArea")
    if logbox != None:
        wait_element_id("userNameInput").send_keys(config.user_data["eid"])
        wait_element_id("passwordInput").send_keys(config.user_data["pass"])
        wait_element_id("submitButton").click()
    
    
kill_task("chrome.exe")
kill_task("chromedriver.exe")
driver = start_browser()

def load_site(site):
    try:
        driver.get(site)
        login_sso()
    except Exception as e:
        restart()
        load_site(site)
        print(e)
    

def restart():
    global driver
    driver = start_browser()
    
    
"""

Finders

"""

def find_by_xpath(path, element=driver):
    try:
        elem = element.find_element_by_xpath(path)
    except ValueError as e:
        print(e)
    return elem


def find_by_id(elem_id,element=driver):
    #element = None
    try:
        elem = element.find_element_by_id(elem_id)
    except ValueError as e:
        print(e)
    return elem


def find_by_class(elem_class,element=driver):
    #element = None
    try:
        elem = element.find_element_by_class_name(elem_class)
    except ValueError as e:
        print(e)
    return elem


def get_children_from(tag, element = driver):
    try:
        elements = element.find_elements_by_tag_name(tag)
        print("Listed " + tag)
    except ValueError as e:
        print(e)        
    return elements

"""

Waits

"""

def wait_element_id(elem_id):
    element = None
    try:
        element = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.ID, elem_id))
        )
        print("Found.")
    except err.TimeoutException as e:
        print(e.msg)
        
    return element

    
def wait_element_xpath(path):
    element = None
    try:
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, path))
        )
        print("Found.")
    except err.TimeoutException as e:
        print(e.msg)
        
    return element


def wait_element_class(elem_class):
    element = None
    try:
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, elem_class))
        )
        print("Found.")
    except err.TimeoutException as e:
        print(e.msg)
        
    return element


def wait_element_clickable(path):
    element = None
    try:
        element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, path))
        )
        print("Found.")
    except ValueError as e:
        print(e)
        
    return element


def wait_element_dissapear(elem_id):
    SHORT_TIMEOUT  = 5   # give enough time for the loading element to appear
    LONG_TIMEOUT = 20  # give enough time for loading to finish
    try:
    # wait for loading element to appear
    # - required to prevent prematurely checking if element
    #   has disappeared, before it has had a chance to appear
        WebDriverWait(driver, SHORT_TIMEOUT
            ).until(EC.presence_of_element_located((By.ID, elem_id )))
    
        # then wait for the element to disappear
        WebDriverWait(driver, LONG_TIMEOUT
            ).until_not(EC.presence_of_element_located((By.ID, elem_id)))
    
    except ValueError as e:
        # if timeout exception was raised - it may be safe to 
        # assume loading has finished, however this may not 
        # always be the case, use with caution, otherwise handle
        # appropriately.
        print(e)


def wait_invisible(element):
    if element != None:
        while element.is_displayed():
            print("Waiting..")
            time.sleep(1)
    else:
        print("No elementx")


def wait_visible(element):
    if element != None:
        while not element.is_displayed():
            print("Waiting..")
            time.sleep(1)
    else:
        print("No elementx")
        
"""

Clicks

"""
def move_to(element):
    Actions(driver).move_to_element(element).perform()
    
    
def click_element(element):
    try:
        #move_to(element)
        #element.location_once_scrolled_into_view
        element.click()
        print("Click.")
    except err.ElementClickInterceptedException:
        #move_to(element)
        print("No click but..")
        enter_to(element)
    except exp.ElementNotInteractableException:
        print("No click but..")
        enter_to(element)


def submit_element(element):
    try:
        element.submit()
    except ValueError as e:
        print(e)


def js_click(element):
    try:
        driver.execute_script("arguments[0].click();", element)
    except ValueError as e:
        print(e)
            
"""

Keys

"""
def select_in(element, text):
    Select(element).select_by_visible_text(text)
    
    
def write_into(element, text):
    if element != None:
        try:
            #element.click()
            element.clear()
            element.send_keys(text)
            
        except ValueError as e:
            print(e)
    else:
        print("No hay elemento pa")
    

def enter_to(element):
    try:
        element.send_keys(Keys.ENTER)
        print("Enter.")
    except ValueError as e:
        print(e)
        
  
def enter_by_xpath(path):
    try:
        driver.find_element_by_xpath(path).send_keys(Keys.ENTER)
        print("Enter.")
    except ValueError as e:
        print(e)


def finale():
    driver.quit()
        

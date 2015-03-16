#from django.test import TestCase
from selenium import webdriver

driver = webdriver.Firefox()
driver.get("http://localhost:8000")

assert 'To-Do' in driver.title

driver.quit()

from selenium import webdriver
import selenium
import time

path = "C:/Program Files (x86)/Google/Chrome/Application/chromedriver/chromedriver.exe"
driver = selenium.webdriver.Chrome(path)
driver.get("http://192.168.2.1")
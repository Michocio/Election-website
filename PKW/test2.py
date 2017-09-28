from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from .models import Gmina

"""Dodaje jedno zero do liczby mieszkańców Warszawy i sprawdzam czy liczba mieszkańców
    Polski wzrosła"""
if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

driver = webdriver.Firefox()
driver.get("http://localhost:8000")
loguj = driver.find_element_by_css_selector("#pasek_login span")
loguj.click()
login = driver.find_element_by_css_selector("#id_login")
haslo = driver.find_element_by_css_selector("#id_haslo")
login.send_keys("michocio")
haslo.send_keys("pass12345")
button = driver.find_element_by_css_selector("#logowanie_okno form input:last-of-type")
button.click()
zalogowany = driver.find_element_by_css_selector("#pasek_login").text
assert u"michocio" in zalogowany

mieszkancy_stare = int(driver.find_element_by_css_selector("#stat span:first-of-type").text)

woj = driver.find_element_by_css_selector("#wojewodztwo")
for option in woj.find_elements_by_tag_name('option'):
    if option.text == 'mazowieckie':
        option.click()
        break

rodzaj = driver.find_element_by_css_selector("#gmina")
for option in rodzaj.find_elements_by_tag_name('option'):
    if option.text == 'Miasto':
        option.click()
        break
min = driver.find_element_by_css_selector("#min")
min.send_keys(77777)

filtr = driver.find_element_by_css_selector("#filtruj_button")
filtr.click()
try:
    wait = WebDriverWait(driver, 10)
except TimeoutException:
   assert 1 == 2
wait.until(lambda driver: driver.find_element_by_css_selector("#tr2"))
zmien = driver.find_element_by_css_selector("#tr2 input:first-of-type")
liczba =int( driver.find_element_by_css_selector("#tr2 input:first-of-type").get_attribute('value'))
zmien.send_keys(0)#Dopisz zero

wyslij = driver.find_element_by_css_selector("#tr2 button")
wyslij.click()

try:
    WebDriverWait(driver, 3).until(EC.alert_is_present(),
                                   'Czekaj aż wyskoczy okno')

    alert = driver.switch_to_alert()
    alert.accept()
except TimeoutException:
   assert 1 == 2


iks = driver.find_element_by_css_selector("#edycja_danych span")
iks.click()


mieszkancy_nowe = int(driver.find_element_by_css_selector("#stat span:first-of-type").text)
assert mieszkancy_nowe == mieszkancy_stare+ 9*liczba
#Przywróć do początkowego stanu
backup = Gmina.objects.get(id = 2)
backup.liczba_mieszkancow = mieszkancy_stare
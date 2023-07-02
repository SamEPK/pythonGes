import requests
from bs4 import BeautifulSoup

import os

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

from selenium.webdriver.support.wait import WebDriverWait



load_dotenv()

username_value = os.getenv("ID")
password_value = os.getenv("PASSWORD")

firefox_options = webdriver.FirefoxOptions()
driver = webdriver.Firefox(options=firefox_options)

driver.get("https://ges-cas.kordis.fr/login")

username = driver.find_element(By.CSS_SELECTOR, "input[name='username']")
password = driver.find_element(By.CSS_SELECTOR, "input[name='password']")

username.send_keys(username_value)
password.send_keys(password_value)

driver.find_element(By.CSS_SELECTOR, "input[name='submit']").click()

time.sleep(2)

driver.get("https://myges.fr/student/student-directory")

time.sleep(2)


# Vérifiez que la connexion a réussi
if login_response.status_code == 200:
    # Maintenant que vous êtes connecté, vous pouvez accéder à la page des notes
    notes_url = "https://myges.fr/student/marks"
    notes_response = session.get(notes_url)

    # Vérifiez que la requête pour les notes a réussi
    if notes_response.status_code == 200:
        # Utilisez BeautifulSoup pour analyser le contenu HTML de la page des notes
        notes_soup = BeautifulSoup(notes_response.content, "html.parser")

        #tbody
        tab = notes_soup.select("ui-datatable-data ui-widget-content")

        # Parcourez les éléments des notes et récupérez les informations souhaitées
        for element in tab:

            ligne = element.select_one(".ui-widget-content ui-datatable-even odd-row").text.strip()
            matiere = element.select_one(".mg_inherit_bg").text.strip()
            #note = element.select_one(".note").text.strip()

            # Faites quelque chose avec les informations récupérées, par exemple, les imprimer
            print("Matière :", matiere)
            #print("Note :", note)
    else:
        print("Échec de la requête pour les notes :", notes_response.status_code)
else:
    print("Échec de la connexion :", login_response.status_code)
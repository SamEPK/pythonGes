import json
import os
import time
import codecs
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

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

driver.get("https://myges.fr/student/student-directory")

time.sleep(2)


def planning():
    driver.get("https://myges.fr/student/planning-calendar")

    wait = WebDriverWait(driver, 10)

    is_planning_present = True
    click_count = 0
    planning_data = []
    while click_count < 4 and is_planning_present:
        try:
            # Cliquez sur la flèche de droite
            driver.find_element(By.ID, "calendar:nextMonth").click()

            # Attendez que le chargement soit terminé
            wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, "span.mg_loadingbar_text")))

            # Vérifiez si l'élément spécifique est présent dans la semaine de l'emploi du temps
            planning = driver.find_elements(By.CSS_SELECTOR, "div.fc-event-inner")
            print(planning)
            click_count += 1
            if not len(planning) == 0:
                is_planning_present = False
                print("La recherche du planning a été effectuée avec succès.")
                print("-------------------------------------------------")

                last_end_time = ""  # Initialisez last_end_time

                for element in planning:
                    title_element = element.find_element(By.CSS_SELECTOR, "div.fc-event-title")
                    time_element = element.find_element(By.CSS_SELECTOR, "div.fc-event-time")
                    title = title_element.text.strip()
                    time = time_element.text.strip()

                    current_end_time = time.split(" - ")[1]  # Récupérer l'heure de fin du cours actuel

                    if last_end_time and current_end_time > last_end_time:
                        print()  # Ajouter un espace entre les jours

                    print("| {:<30} | {:<12} |".format(title, time))

                    last_end_time = time.split(" - ")[
                        1]  # Mettre à jour last_end_time avec l'heure de fin du cours actuel
                for element in planning:
                    title_element = element.find_element(By.CSS_SELECTOR, "div.fc-event-title")
                    time_element = element.find_element(By.CSS_SELECTOR, "div.fc-event-time")
                    title = title_element.text.strip()
                    time = time_element.text.strip()
                    planning_data.append({"Title": title, "Time": time})  # Ajoutez les données du cours à la liste
                print("-------------------------------------------------")
                planning_json = json.dumps(planning_data)

                # Imprimez la représentation JSON
                print(planning_json)
                with codecs.open("planning.json", "w", "utf-8") as file:
                    file.write(planning_json)
            else:
                print("Aucun planning n'a été trouvé dans la semaine.")
        except Exception as e:
            print(e)
            is_planning_present = False
            break

def notes():
    driver.get("https://myges.fr/student/marks")

    # Récupération de tous les champs de texte dans la div
    text_fields = driver.find_elements(By.CSS_SELECTOR,
                                       ".mg_content .mg_inherit_bg span, .mg_content table tbody td:not(.mg_inherit_bg)")

    # Parcours des champs de texte et affichage
    for field in text_fields:
        print(field.text)
    data_list = []
    for field in text_fields:
        data_list.append(field.text)
    # Conversion de la liste en JSON
    notes_json = json.dumps(data_list)

    # Imprimer la représentation JSON
    print(notes_json)

    # Écriture des données JSON dans un fichier
    with codecs.open("notes.json", "w", "utf-8") as file:
        file.write(notes_json)

def eleves():
    driver.get("https://myges.fr/student/student-directory")

    # Récupération de tous les champs de texte dans la div
    data_list = []
    while True:
        # Parcours des champs de texte et récupération des noms et des images
        elements = driver.find_elements(By.CSS_SELECTOR, ".mg_content .mg_directory_block_container")
        for element in elements:
            name_element = element.find_element(By.CSS_SELECTOR, ".mg_directory_text")
            image_element = element.find_element(By.CSS_SELECTOR, ".mg_directory_container img")
            name = name_element.text
            image_url = image_element.get_attribute("src")
            data_list.append({"name": name, "image": image_url})

        # Recherche du bouton "Suivant" pour passer à la page suivante
        next_button = driver.find_element(By.CSS_SELECTOR, ".ui-paginator-next")
        if "ui-state-disabled" in next_button.get_attribute("class"):
            # Si le bouton "Suivant" est désactivé, on sort de la boucle
            break
        else:
            # Sinon, on clique sur le bouton "Suivant" pour passer à la page suivante
            next_button.click()
            # Attente pour laisser le temps à la page suivante de se charger
            time.sleep(2)

    # Conversion de la liste en JSON
    eleves_json = json.dumps(data_list, ensure_ascii=False)

    # Affichage de la représentation JSON
    print(eleves_json)

    # Écriture des données JSON dans un fichier UTF-8
    with codecs.open("eleves.json", "w", "utf-8") as file:
        file.write(eleves_json)

planning()
notes()
eleves()


driver.quit()
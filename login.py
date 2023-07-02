import os
import time
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

time.sleep(2)

driver.get("https://myges.fr/student/student-directory")

time.sleep(2)

driver.get("https://myges.fr/student/planning-calendar")

wait = WebDriverWait(driver, 10)

is_planning_present = True
click_count = 0

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

                last_end_time = time.split(" - ")[1]  # Mettre à jour last_end_time avec l'heure de fin du cours actuel
            print("-------------------------------------------------")
        else:
            print("Aucun planning n'a été trouvé dans la semaine.")
    except Exception as e:
        print(e)
        is_planning_present = False
        break

driver.quit()
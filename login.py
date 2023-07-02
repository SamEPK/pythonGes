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

        # Attendez 2 secondes entre chaque clic sur le bouton "next"
        time.sleep(2)

        # Vérifiez si l'élément spécifique est présent dans la semaine de l'emploi du temps
        is_planning_present = driver.find_elements(By.CSS_SELECTOR, "div.fc-event-inner")

        click_count += 1
    except Exception:
        is_planning_present = False
        break

if not is_planning_present:
    print("Erreur : Aucun planning n'a été trouvé dans la semaine.")
else:
    print("La recherche du planning a été effectuée avec succès.")

exec(open('data_planning.py').read())


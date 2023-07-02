import requests
from bs4 import BeautifulSoup

# Faites une requête HTTP pour obtenir le contenu de la page
url = "https://myges.fr/student/planning-calendar"
response = requests.get(url)

# Vérifiez que la requête a réussi
if response.status_code == 200:
    # Utilisez BeautifulSoup pour analyser le contenu HTML de la page
    soup = BeautifulSoup(response.content, "lxml")

    # Trouvez les éléments du planning en utilisant les sélecteurs CSS ou les méthodes de BeautifulSoup

    planning_elements = [soup.select(".fc-view fc-view-agendaWeek fc-agenda")]

    # Parcourez les éléments du planning et récupérez les informations souhaitées
    for element in planning_elements:

        date = element.select_one(".fc-event-time").text.strip()
        description = element.select_one(".fc-event-title").text.strip()

        # Faites quelque chose avec les informations récupérées, par exemple, les imprimer
        print("Date :", date)
        print("Description :", description)
else:
    print("Échec de la requête :", response.status_code)

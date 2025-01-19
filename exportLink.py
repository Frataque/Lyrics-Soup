import requests
from bs4 import BeautifulSoup

# URL de l'album sur Genius
url = "https://genius.com/albums/So-la-lune/Tsuki"

# Envoyer une requête pour récupérer le contenu de la page
response = requests.get(url)

# Vérifie si la requête est réussie
if response.status_code == 200:
    # Parse le contenu HTML de la page
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Trouver toutes les balises <a> avec la classe "u-display_block"
    song_links = soup.find_all('a', class_='u-display_block')
    count = 0
    # Extraire les URLs des chansons
    for link in song_links:
        
        count += 1
        print(count)
        print(link['href'])
else:
    print(f"Erreur : Impossible d'accéder à la page (statut {response.status_code})")

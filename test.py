from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from dotenv import load_dotenv
import os
from supabase import create_client, Client  # pip install supabase

# Paramètres de connexion Supabase
load_dotenv()
SUPABASE_URL =  os.getenv("DATABASE_URL")  # Remplacez par votre URL Supabase
SUPABASE_KEY =  os.getenv("KEY")  # Remplacez par votre clé API

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Configurer Chrome en mode headless
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://genius.com/artists/So-la-lune/songs")
wait = WebDriverWait(driver, 20)

# Cliquer sur le bouton pour accepter les cookies
try:
    cookie_button = wait.until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler")))
    cookie_button.click()
    time.sleep(1)
except Exception as e:
    print("Bouton cookies introuvable ou non cliquable :", e)

# Attendre que le conteneur de la liste soit présent
try:
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "ul.ListSection-desktop-sc-2bca79e6-8.eYDiSo")))
except Exception as e:
    print("Conteneur de la liste non trouvé :", e)

# Scroller pour charger tous les éléments
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)  # Temps d'attente adapté à votre connexion
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# Extraire les éléments de la liste (titres et liens)
song_elements = driver.find_elements(By.CSS_SELECTOR, "ul.ListSection-desktop-sc-2bca79e6-8.eYDiSo li.ListItem-sc-4f1bc3d5-0.ZvWhZ")

results = []
for li in song_elements:
    try:
        a_tag = li.find_element(By.TAG_NAME, "a")
        lien = a_tag.get_attribute("href")
        titre_element = a_tag.find_element(By.CSS_SELECTOR, "h3.ListItem-sc-4f1bc3d5-4.gpuzaZ")
        titre = titre_element.text.strip()
        if titre and lien:
            results.append({"titre": titre, "lien": lien})
    except Exception as e:
        continue

driver.quit()

# Préparer les données pour insertion dans la table "songs" de Supabase.
# Ici, nous insérons uniquement le titre, l'URL et un flag scraped à False.
songs_to_insert = [
    {"title": song["titre"], "url": song["lien"], "scraped": False}
    for song in results
]

# Insérer les données dans Supabase (opération bulk)
response = supabase.table("songs").insert(songs_to_insert).execute()

# Afficher la réponse de Supabase pour vérification
print("Réponse Supabase :", response)

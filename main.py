import psycopg2
from dotenv import load_dotenv
import os

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Récupérer les informations de connexion
USER = os.getenv("user")
PASSWORD = os.getenv("password")
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")

# Connexion à la base de données
try:
    connection = psycopg2.connect(
        user=USER,
        password=PASSWORD,
        host=HOST,
        port=PORT,
        dbname=DBNAME
    )
    print("Connexion réussie avec le Transaction Pooler !")
    
    # Créer un curseur pour exécuter des requêtes SQL
    cursor = connection.cursor()
    
    # Exemple : récupérer l'heure actuelle
    cursor.execute("SELECT NOW();")
    result = cursor.fetchone()
    print("Heure actuelle :", result)

    # Fermer le curseur et la connexion
    cursor.close()
    connection.close()
    print("Connexion fermée.")

except Exception as e:
    print(f"Erreur lors de la connexion : {e}")

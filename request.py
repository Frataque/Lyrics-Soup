import psycopg2
from dotenv import load_dotenv
import os

# Charger les variables d'environnement
load_dotenv()

# Connexion à la base de données
connection = psycopg2.connect(
    user=os.getenv("user"),
    password=os.getenv("password"),
    host=os.getenv("host"),
    port=os.getenv("port"),
    dbname=os.getenv("dbname")
)

cursor = connection.cursor()

# Requête pour récupérer toutes les informations d'une chanson
query = """
SELECT 
    songs.id AS song_id,
    songs.title AS song_title,
    albums.name AS album_name,
    albums.artist AS album_artist,
    albums.release_date AS album_release_date,
    songs.producer AS producer_name,
    songs.lyrics AS song_lyrics,
    songs.release_date AS song_release_date,
    COALESCE(ARRAY_AGG(featurings.artist_name), ARRAY[]::VARCHAR[]) AS featurings
FROM 
    songs
LEFT JOIN albums ON songs.album_id = albums.id
LEFT JOIN featurings ON songs.id = featurings.song_id
GROUP BY 
    songs.id, albums.id;
"""

# Exécuter la requête
cursor.execute(query)

# Récupérer les résultats
results = cursor.fetchall()

# Afficher les résultats
for row in results:
    print("ID de la chanson :", row[0])
    print("Titre :", row[1])
    print("Album :", row[2])
    print("Artiste :", row[3])
    print("Date de sortie de l'album :", row[4])
    print("Producteur :", row[5])
    print("Paroles :", row[6])
    print("Date de sortie de la chanson :", row[7])
    print("Featurings :", row[8])  # Liste des artistes en featuring
    print("-" * 40)


# Fermer le curseur et la connexion
cursor.close()
connection.close()

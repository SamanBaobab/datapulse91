import psycopg2
import os
from dotenv import load_dotenv

from datapulse91.database.db_config import engine
from datapulse91.database.db_models import Base

# Charger les variables d'environnement
load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

def create_database():
    """ Vérifie si la base existe et la crée si elle n'existe pas """
    try:
        conn = psycopg2.connect(
            dbname="postgres", user=DB_USER,
            password=DB_PASS, host=DB_HOST, port=DB_PORT
        )
        conn.autocommit = True
        cursor = conn.cursor()

        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{DB_NAME}';")
        exists = cursor.fetchone()

        if not exists:
            cursor.execute(f"CREATE DATABASE {DB_NAME};")
            print(f"✅ Base de données '{DB_NAME}' créée avec succès.")
        else:
            print(f"🔹 La base '{DB_NAME}' existe déjà.")

        cursor.close()
        conn.close()
    except Exception as e:
        print(f"❌ Erreur lors de la création de la base : {e}")

def create_tables():
    """ Crée les tables dans la base de données """
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Tables créées avec succès !")
    except Exception as e:
        print(f"❌ Erreur lors de la création des tables : {e}")

if __name__ == "__main__":
    create_database()  # Crée la base si elle n'existe pas
    create_tables()  # Crée les tables dans la base
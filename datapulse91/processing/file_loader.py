import csv
import json
from datapulse91.logging_config import logger
from pathlib import Path

def detect_file_type_path(filepath):
    """
    Detecte automatiquement le type de fichier en fonction de son
    extension
    :param filepath:
    :return:
    """
    try:
        filepath = Path(filepath)
        extension = filepath.suffix.lower()
        file_types = {
            ".json":"json",
            ".csv":"csv",
            ".txt":"txt",
        }
        return file_types.get(extension, None)
    except Exception as e :
        logger.error(f"Erreur lors de la detection du fichier {filepath} : {e}")
def load_text_file(filepath):
    """
    Lit un fichier texte ligne par ligne en utilisant un générateur
    :param filepath: chemin fichier
    :return: ligne du fichier
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            for line in file:
                yield line.strip()
    except Exception as e :
        logger.error(f"Erreur de lecture TXT {filepath}: {e}")
def load_csv_file(filepath, delimiter=","):
    """
    Lit un fichier csv et retourne un générateur de lignes
    sous forme de dictionnaire
    :param filepath: chemin fichier
    :param delimiter: séparateur
    :return: dictionnaire
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as file :
            reader = csv.DictReader(file, delimiter=delimiter )
            for row in reader :
                yield row
    except Exception as e :
        logger.error(f"Erreur lecture fichier csv {filepath}: {e}")


def load_json_file(filepath):
    """
    Charge un fichier JSON et retourne son contenu
    :param filepath: chemin fichier
    :return: objet désérialiser
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as file :
            return json.load(file)
    except Exception as e :
        logger.error(f"Erreur lecture fichier json {filepath}; {e}")

def load_file(filepath):
    file_type = detect_file_type_path(filepath)
    # Dictionnaire des loaders
    loaders = {
        "csv": load_csv_file,
        "json":load_json_file,
        "txt":load_text_file
    }
    if file_type:
        return loaders.get(file_type)(filepath)
    else:
        return None


if __name__ == "__main__":
    pass

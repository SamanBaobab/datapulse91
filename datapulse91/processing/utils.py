import os.path
import time

from datapulse91.logging_config import logger
import sys
from datapulse91.processing import file_loader

def validate_file(file_path):
    """
    Vérifier l'existence et la lisibilité du fichier
    :param file_path: nom du fichier
    :return:
    """
    if not os.path.exists(file_path):
        logger.error(f"Le fichier {file_path} n'existe pas")
        sys.exit(1)
    if not os.access(file_path, os.R_OK):
        logger.error(f"Le fichier {file_path} existe mais pas lisible")
        sys.exit(1)


def detect_and_load_file(file_path, verbose):
    """
    Detecte le type et charge les données
    :param file_path: chemin du fichier
    :param verbose: permet de définir un niveau DEBUG sur logger
    :return: data: données du fichier
    """
    file_type = file_loader.detect_file_type_path(file_path)
    logger.info(f"Type detecté : {file_type.upper() if file_type else 'Inconnu'} ")

    start_time = time.time()
    data = list(file_loader.load_file(file_path))
    elapsed_time = time.time() - start_time

    logger.debug(f"Temps de chargement: {elapsed_time:.3f} sec")
    logger.debug(f"Nombres de lignes chargées: {len(data) if data else 0}")

    if not data:
        logger.warning(f"Aucun contenu valide extrait de {file_path}")

    return data


def display_data(data, limit):
    """
    Affiche les première lignes du fichier
    :param data: données du fichier
    :param limit: nombre max de lignes à afficher
    :return:
    """
    logger.info(f"Apercu des données")
    for i, line in enumerate(data[:limit]):
        print(line)
        print()
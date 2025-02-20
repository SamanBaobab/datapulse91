import logging
import os.path
import time
from datapulse91.logging_config import logger
import sys
from datapulse91.processing import file_loader

def setup_logging(verbose):
    """
    Execution des logs en DEBUG
    :param verbose: argument verbose pour gérer les informations détaillées
    """
    # VERBOSE : utile pour débogage + suivi des performances
    # Si verbose= True on passe le logger en mode DEBUG (en développement car en prod verbose est à false)
    if verbose:
        logger.setLevel(logging.DEBUG)
        logger.debug("Mode verbose activé")


def validate_file(file_path):
    """
    Vérifier l'existence et la lisibilité du fichier
    :param file_path: nom du fichier
    :raises FileNotFoundError: si le fichier n'existe pas
    :raises PermissionError: si le fichier n'est pas lisible
    """
    if not os.path.exists(file_path):
        logger.error(f"Le fichier {file_path} n'existe pas")
        #sys.exit(1)
        raise FileNotFoundError(f"Le fichier {file_path} n'existe pas")
    if not os.access(file_path, os.R_OK):
        logger.error(f"Le fichier {file_path} existe mais pas lisible")
        #sys.exit(1)
        raise PermissionError(f"Le fichier {file_path} existe mais pas lisible")


def detect_and_load_file(file_path, verbose):
    """
    Detecte le type de fichier et charge les données
    :param file_path: chemin du fichier
    :param verbose: permet de définir un niveau DEBUG dans les logs
    :return: data: liste contenant les données du fichier
    :raises ValueError: si le type de fichier est inconnu
    :raises RuntimeError: si le chargement échoue
    """
    setup_logging(verbose)

    file_type = file_loader.detect_file_type_path(file_path)
    logger.info(f"Type detecté : {file_type.upper() if file_type else 'Inconnu'} ")

    if not file_type:
        raise ValueError(f"Le type fichier de {file_path} est inconnu")

    start_time = time.time()
    data = list(file_loader.load_file(file_path))
    elapsed_time = time.time() - start_time

    logger.debug(f"Temps de chargement: {elapsed_time:.3f} sec")
    logger.debug(f"Nombres de lignes chargées: {len(data) if data else 0}")

    if not data:
        logger.warning(f"Aucun contenu valide extrait de {file_path}")
        raise RuntimeError(f"Le fichier {file_path} semble vide ou illisible")
    return data

def filter_data(data, filter_text):
    """
    Filtre les lignes contenant un texte donné
    :param data: Liste des lignes à filtrer
    :param filter_text: Mot-clé à rechercher
    :return: Liste des lignes filtrées
    :raises ValueError: Si aucune ligne ne correspond
    """
    if not filter_text:
        logger.debug("Aucun mot clé fourni, retour des données brutes")
        return data

    filtered_data = [line for line in data if filter_text.lower() in str(line).lower()]

    if not filtered_data:
        logger.warning(f"Aucune ligne ne contient {filter_text}")
        raise ValueError(f"Aucune ligne ne contient {filter_text}")

    logger.info(f"{len(filtered_data)} lignes trouvées après filtrage")
    return filtered_data


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
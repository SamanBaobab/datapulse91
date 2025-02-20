from datapulse91.processing.utils import detect_and_load_file, display_data, filter_data
from datapulse91.logging_config import logger


def filter_data_command(args):
    """
    Fonction executée pour la commande filter
    :param args: arguments associés à la commande filter
    """
    try:
        print(f"Recherche dans {args.file} du mot-clé {args.keyword}")
        # Charger les données
        data = detect_and_load_file(args.file, args.verbose)

        # Appliquer le filtre
        data = filter_data(data, args.keyword)

        # Afficher les résultats
        limit = len(data)
        display_data(data, limit)

    except (FileNotFoundError, PermissionError, ValueError, RuntimeError) as e:
        logger.error(f"Erreur dans filter_file: {e}")
        print(f"Erreur: {e}")

def register_subcommand(subparsers):
    """
    Enregistre la sous commande filter
    :param subparsers: La sous commande de parser
    """
    parser=subparsers.add_parser("filter", help="Recherche et affiche les lignes filtrées")
    parser.add_argument("--file", type=str, required=True, help="Fichier à analyser")
    parser.add_argument("--keyword", type=str, required=True, help="Mot clé à rechercher")
    parser.add_argument("--verbose", action="store_true", help="Mode verbeux (DEBUG) ")
    parser.set_defaults(func=filter_data_command)

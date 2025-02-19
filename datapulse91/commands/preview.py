from datapulse91.processing.utils import validate_file, detect_and_load_file, display_data


def preview_file(args):
    """
    Affiche un apercu du fichier et ses informations
    :param args:
    :return:
    """

    # Validation du fichier via validate_file() (qui se trouve dans utils)
    validate_file(args.file)

    # Obtenir des infos sur le fichier avec os (A FAIRE)

    # Charger les données
    data = detect_and_load_file(args.file, args.verbose)

    # Afficher un apercu des données
    display_data(data, args.read)

def register_subcommand(subparsers):
    '''
    Enregistre la sous commande preview
    :param subparsers:
    :return:
    '''
    parser = subparsers.add_parser("preview", help="Affiche un apercu du fichier")
    parser.add_argument("--file", type=str, required=True, help="Chemin du ficher à prévisualiser")
    parser.add_argument("--read", type=int, default=5, help="Nombre de lignes à afficher")
    parser.add_argument("--info", action="store_true", help="Afficher les infos")
    parser.add_argument("--verbose", action="store_true", help="Mode verbeux")
    parser.set_defaults(func=preview_file)

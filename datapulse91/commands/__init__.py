import importlib
import pkgutil

def load_subcommands(subparsers):
    """
    Charge automatiquement les fichiers dans commands et enregistre leurs sous-commandes
    :param subparsers: sous-commande
    :return:
    """
    for _, module_name, _ in pkgutil.iter_modules(__path__):
        module = importlib.import_module(f"datapulse91.commands.{module_name}")
        # Vérifie si le module importé possède une fonction register_sbcommand()
        # Si oui, cette fonction est appelée pour enregistrer la sous commande dans subparsers
        if hasattr(module, "register_subcommand"):
            module.register_subcommand(subparsers)


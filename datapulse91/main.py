import argparse
from datapulse91.commands import load_subcommands
def main():
    parser = argparse.ArgumentParser(description="DataPulse avec les sous commandes")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Charger automatiquement les sous commandes
    load_subcommands(subparsers)

    # Parser les arguments
    args = parser.parse_args()

    # Executer la fonction asscoiée
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()

if __name__== "__main__":
    main()

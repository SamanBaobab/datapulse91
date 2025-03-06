import argparse
import os
import json
from datapulse91.analysis.clients.clients_analyze import analyze_clients
from datapulse91.analysis.server_logs.data_summary import analyze_server_logs
from datapulse91.analysis.transactions.transactions_analyze import analyze_transactions
from datapulse91.logging_config import logger

def analyze_clients_cli(args):
    """
    Exécute l'analyse des clients depuis la CLI.
    """
    try:
        results = analyze_clients(args.file)
        print(results)  # Affichage propre
    except Exception as e:
        logger.error(f"Erreur dans analyze_clients_cli : {e}")

def analyze_transactions_cli(args):
    """
    Exécute l'analyse des transactions depuis la CLI.
    """
    try:
        results = analyze_transactions(args.file)
        print(results)
    except Exception as e:
        logger.error(f"Erreur dans analyze_transactions_cli : {e}")

def analyze_server_cli(args):
    """
    Exécute l'analyse des logs serveur depuis la CLI.
    """
    try:
        results = analyze_server_logs(args.file)
        print(results)
    except Exception as e:
        logger.error(f" Erreur dans analyze_server_cli : {e}")

def register_subcommand(subparsers):
    """
    Enregistre les sous-commandes d'analyse.
    """
    # Commande pour analyser les clients
    parser_clients = subparsers.add_parser("analyze_clients", help="Analyse les données des clients.")
    parser_clients.add_argument("--file", type=str, required=True, help="Chemin du fichier des clients.")
    parser_clients.set_defaults(func=analyze_clients_cli)

    # Commande pour analyser les transactions
    parser_transactions = subparsers.add_parser("analyze_transactions", help="Analyse les transactions.")
    parser_transactions.add_argument("--file", type=str, required=True, help="Chemin du fichier des transactions.")
    parser_transactions.set_defaults(func=analyze_transactions_cli)

    # Commande pour analyser les logs serveur
    parser_server = subparsers.add_parser("analyze_server", help="Analyse les logs serveur.")
    parser_server.add_argument("--file", type=str, required=True, help="Chemin du fichier des logs serveur.")
    parser_server.set_defaults(func=analyze_server_cli)
import pandas as pd
import json
from sqlalchemy.orm import Session
from datetime import datetime

from datapulse91.database.db_config import get_db
from datapulse91.database.db_queries import insert_client, insert_transaction


def import_clients(csv_path):
    """ Importe les clients en base de données depuis un fichier CSV """
    db: Session = next(get_db())

    df = pd.read_csv(csv_path, parse_dates=["inscription", "derniere_activite"])

    # ✅ Correction : Renommer `client_id` en `id`
    df.rename(
        columns={"client_id": "id", "inscription": "inscription_date", "vip": "is_vip", "montant": "montant_total"},
        inplace=True)

    # ✅ Supprimer `id` car PostgreSQL va l’auto-incrémenter
    df = df.drop(columns=["id"], errors="ignore")

    for _, row in df.iterrows():
        insert_client(db, row.to_dict())  # ✅ Maintenant, l'`id` n'est plus fourni

    print(f"✅ {len(df)} clients importés avec succès.")

def import_transactions(json_path):
    """ Importe les transactions en base de données depuis un fichier JSON """
    db: Session = next(get_db())

    with open(json_path, "r", encoding="utf-8") as f:
        transactions_list = json.load(f)

    for transaction in transactions_list:
        transaction_data = {
            "id": transaction["transaction_id"],
            "date": datetime.strptime(transaction["date"], "%Y-%m-%d"),
            "client_id": transaction["client"]["id"],
            "produit": transaction["produit"],
            "montant": transaction["montant"],
            "statut_paiement": transaction["statut_paiement"],
            "moyen_paiement": transaction["moyen_paiement"]
        }
        insert_transaction(db, transaction_data)

    print(f"✅ {len(transactions_list)} transactions importées avec succès.")

if __name__ == "__main__":
    pass
    #import_clients("../../data/clients.csv")
    #import_transactions("../../data/transactions.json")
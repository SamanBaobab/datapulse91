from collections import Counter
from datapulse91.logging_config import logger
import pandas as pd

from datapulse91.processing.file_loader import load_file


def analyze_clients(csv_path):
    total_clients = 0
    top_clients= Counter()
    inactive_clients_count=0
    oldest_inactive_clients = Counter()
    client_categories ={
        "petits_acheteurs":0,
        "moyens_acheteurs":0,
        'gros_acheteurs':0
    }
    client_spending = Counter()

    # Chargement des données
    transactions = load_file(csv_path)

    chunk=[]
    for row in transactions:
        chunk.append(row)

        if len(chunk) >= 1000:
            df = pd.DataFrame(chunk)
            chunk=[]

            if "client_id" not in df.columns :
                logger.warning(f"Colonnes manquantes, chunk ignoré ")
                continue

            df["derniere_activite"]=pd.to_datetime(df["derniere_activite"], errors="coerce")
            df["montant"]= pd.to_numeric(df["montant"], errors="coerce").fillna(0)

            total_clients += df["client_id"].nunique()

            inactifs = df.loc[df["derniere_activite"].notna() & (df["derniere_activite"] < pd.Timestamp("2024-01-01") ), ["client_id", "derniere_activite"]]
            inactive_clients_count += len(inactifs)
            oldest_inactive_clients.update(inactifs["derniere_activite"].astype(str))

            top_clients.update(df["client_id"])
            spending_per_client = df.groupby("client_id")["montant"].sum().to_dict()
            client_spending.update(spending_per_client)

            for client_id, montant_total  in client_spending.items():
                if montant_total < 100 :
                    client_categories["petits_acheteurs"]+=1
                elif montant_total < 500 :
                    client_categories["moyens_acheteurs"]+=1
                else :
                    client_categories["gros_acheteurs"]+=1


            top_clients = dict(top_clients.most_common(5))
            oldest_inactive_clients = dict(oldest_inactive_clients.most_common(1))

            return {
                "total_clients":total_clients,
                "top_clients":top_clients,
                "inactive_clients_count":inactive_clients_count,
                "oldest_inactive_clients": oldest_inactive_clients,
                "client_categories": client_categories
            }

if __name__ == "__main__":
    print(analyze_clients("../../../data/clients.csv"))
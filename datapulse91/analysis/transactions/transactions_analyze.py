from collections import Counter

from datapulse91.logging_config import logger

import numpy as np
import pandas as pd

from datapulse91.processing.file_loader import load_file


def analyze_transactions(json_path, chunk_size=1000):
    total_transactions = 0
    total_amount = 0
    montant_list = []

    status_counts = Counter()
    payment_methods = Counter()
    product_counts = Counter()
    transactions_per_client = Counter()
    ca_per_month = Counter()
    high_value_transactions = []

    transactions = load_file(json_path)

    chunk = []
    for transaction in transactions:
        chunk.append(transaction)
        if len(chunk) >= chunk_size:
            df = pd.DataFrame(chunk)
            chunk = []  # Réinitialiser pour le prochain chunk

            # Vérification des colonnes nécessaires
            required_columns = ["montant", "date"]
            missing_columns = [col for col in required_columns if col not in df.columns]

            if missing_columns:
                logger.warning(f"Colonnes manquantes dans ce chunk : {missing_columns}, passage au suivant.")
                continue  #  Ignore le chunk si les colonnes obligatoires sont absentes

            # Conversion des colonnes avec gestion des erreurs
            df["montant"] = pd.to_numeric(df["montant"], errors="coerce")  #  Convertir en numérique
            df["date"] = pd.to_datetime(df["date"], errors="coerce")  #  Convertir la date en datetime

            df.dropna(subset=["montant", "date"], inplace=True)  #  Supprime les transactions invalides

            total_transactions += len(df)
            total_amount += df["montant"].sum()  #  NumPy gère déjà les NaN dans sum()
            montant_list.extend(df["montant"].tolist())  #  Conversion plus propre

            #  Regroupement des transactions par mois
            df["year_month"] = df["date"].dt.to_period("M")  #  Transforme en format YYYY-MM
            ca_per_month.update(df.groupby("year_month")["montant"].sum().to_dict())

            #  Comptage des différentes valeurs
            if "statut_paiement" in df.columns:
                status_counts.update(df["statut_paiement"].dropna())

            if "moyen_paiement" in df.columns:
                payment_methods.update(df["moyen_paiement"].dropna())

            if "produit" in df.columns:
                product_counts.update(df["produit"].dropna())

            #  Gestion robuste des clients
            if "client" in df.columns:
                df["client_id"] = df["client"].apply(
                    lambda x: x.get("id", None) if isinstance(x, dict) else None
                )
                transactions_per_client.update(df["client_id"].dropna())

    # Calcul final avec NumPy (évite crash si aucune transaction valide)
    if montant_list:
        montant_array = np.array(montant_list)  #  Convertir en tableau NumPy
        mean_amount = np.mean(montant_array)
        median_amount = np.median(montant_array)
        threshold_value = np.percentile(montant_array, 95)  #  95e percentile
        high_value_transactions = montant_array[montant_array > threshold_value]
    else:
        mean_amount, median_amount, std_dev, high_value_transactions = 0, 0, 0, []

    return {
        "total_transactions": total_transactions,
        "total_amount": total_amount,
        "mean_amount": mean_amount,
        "median_amount": median_amount,
        "status_counts": dict(status_counts),
        "transactions_per_client": dict(transactions_per_client),
        "outlier_transactions_count": len(high_value_transactions),
        "top_products": dict(product_counts.most_common(5)),
        "payment_methods": dict(payment_methods),
        "ca_per_month": dict(ca_per_month),
    }


if __name__=="__main__":
    print(analyze_transactions("../../../data/transactions.json"))
from sqlalchemy.orm import Session

from datapulse91.database.db_models import Client, Transaction


def insert_client(db: Session, client_data: dict):
    """ Insère un client en base de données """
    client = Client(**client_data)
    db.add(client)
    db.commit()
    db.refresh(client)
    return client

def insert_transaction(db: Session, transaction_data: dict):
    """ Insère une transaction en base de données """
    transaction = Transaction(**transaction_data)
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction
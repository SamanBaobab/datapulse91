from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, UniqueConstraint
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Client(Base):
    """ Table des clients """
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, autoincrement=True)  # ✅ Auto-incrémentation
    nom = Column(String, nullable=False)
    prenom = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)  # ✅ UNIQUE(email)
    telephone = Column(String)
    inscription_date = Column(DateTime)
    is_vip = Column(Boolean, default=False)
    derniere_activite = Column(DateTime)
    montant_total = Column(Float, default=0.0)

class Transaction(Base):
    """ Table des transactions """
    __tablename__ = "transactions"

    id = Column(String, primary_key=True)  # ID transaction ex: TXN00123
    date = Column(DateTime, nullable=False)
    client_id = Column(Integer, nullable=False)  # 🔗 Clé étrangère vers Client
    produit = Column(String, nullable=False)
    montant = Column(Float, nullable=False)
    statut_paiement = Column(String, nullable=False)
    moyen_paiement = Column(String, nullable=False)
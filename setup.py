# Fichier central pour distribuer un projet python sous forme de package installable.
# D'installer les dépendances automatiquement
# D'enregistrer des scripts pour éxecution en ligne de commande
# De gérer la compatibilité du projet
# Publier le package du PyPi (the python Package Index)

from setuptools import setup, find_packages

setup(
    name="datapulse91",
    version="1.0.0",
    description="Outil d'analyse de données",
    author="Heeralall",
    packages=find_packages(), # détecter automatiquement les packages dans le projet
    entry_points={
        "console_scripts":[
            "datapulse91 = datapulse91.main:main", # monprojet = package.main:main
        ]
    }
)

# Rendre l'application installable et executable en cli
# Création d'un lien symbolique entre votre code source et l'installation python
# pip install -e . (tester votre package localement)
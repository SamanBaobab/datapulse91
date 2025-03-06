import os.path
from abc import ABC, abstractmethod
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

from datapulse91.logging_config import logger


class BaseVisualizer(ABC):
    """
    Classe Abstraite pour gérer la visualisation
    des données analytiques
    """
    def __init__(self, analysis_results:dict):
        self._results = analysis_results

    @abstractmethod
    def plot(self):
        pass

    def _setup_figure(self, title : str, figsize=(8,5)):
        sns.set_theme(style="whitegrid")
        fig, ax = plt.subplots(figsize=figsize)
        ax.set_title(title, fontsize=14, fontweight="bold")
        return fig, ax

    @abstractmethod
    def get_plots(self):
        pass

    def generate_pdf(self, filename="report.pdf"):
        """
        Génère un rapport PDF contenant toutes les visualisations du visualiseur.

        :param filename: Nom du fichier PDF.
        """
        try:
            # Définition du chemin du dossier reports
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            reports_dir = os.path.join(base_dir, "reports")
            os.makedirs(reports_dir, exist_ok=True)  # Création du dossier s'il n'existe pas
            filepath = os.path.join(reports_dir, filename)

            with PdfPages(filepath) as pdf:
                for plot_method in self.get_plots():
                    result = plot_method()

                    if result is None or result == (None, None):  # Vérification des résultats
                        logger.warning(f"Graphique ignoré : {plot_method.__name__} (aucune donnée)")
                        continue

                    fig, ax = result
                    pdf.savefig(fig)  # Sauvegarde dans le PDF
                    plt.close(fig)  # Fermeture de la figure après ajout

            logger.info(f"Rapport PDF généré : {filepath}")

        except Exception as e:
            logger.error(f"Erreur lors de la génération du PDF : {e}", exc_info=True)
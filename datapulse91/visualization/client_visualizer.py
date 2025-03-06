from datapulse91.logging_config import logger
from datapulse91.visualization.base_visualizer import BaseVisualizer
import seaborn as sns
import matplotlib.pyplot as plt

class ClientVisualizer(BaseVisualizer):
    """
    Classe pour visualiser les résultats de l'analyse des clients.
    """

    def plot(self, plot_type=None):
        """
        Affiche un graphique spécifique ou tous si `plot_type` est None.

        :param plot_type: Type de graphique à afficher (client_distribution, inactive_clients).
        """
        if plot_type == "client_distribution":
            fig, ax = self.plot_clients_distribution()
        elif plot_type == "inactive_clients":
            fig, ax = self.plot_inactive_clients()
        else:
            logger.info("📊 Affichage de tous les graphiques clients...")
            for plot_method in self.get_plots():
                fig, ax = plot_method()
                if fig:
                    plt.show()
            return

        if fig:
            plt.show()

    def get_plots(self):
        """
        Retourne les méthodes de visualisation à exporter en PDF.

        :return: Liste des méthodes de tracé.
        """
        return [self.plot_clients_distribution, self.plot_inactive_clients]

    def plot_clients_distribution(self):
        """
        Affiche la répartition des clients par catégorie.
        """
        try:
            client_categories = self._results.get("client_categories", {})

            if not client_categories:
                logger.warning("Aucune donnée pour la répartition des clients.")
                return None, None

            fig, ax = self._setup_figure("Répartition des clients", figsize=(6, 6))
            labels = list(client_categories.keys())
            sizes = list(client_categories.values())

            ax.pie(sizes, labels=labels, autopct="%1.1f%%", colors=sns.color_palette("muted"))
            logger.info("Graphique 'Répartition des clients' généré.")
            return fig, ax

        except Exception as e:
            logger.error(f"Erreur lors de la création du graphique 'Répartition des clients' : {e}", exc_info=True)
            return None, None

    def plot_inactive_clients(self):
        pass

# Le pattern Factory est design pattern de création qui permet de centraliser et simplifier
# la création d'objets sans exposer la logique de leur instanciation
from datapulse91.visualization.client_visualizer import ClientVisualizer
from datapulse91.visualization.transaction_visualizer import TransactionVisualizer


class VisualizerFactory:
    """
    Fabrique qui retourne le bon visualiseur en fonction des
    données fournies
    """
    @staticmethod
    def get_visualizer(analysis_results: dict, analysis_type:str):
        if analysis_type == "transactions":
            return TransactionVisualizer(analysis_results)
        elif analysis_type == "clients":
            return ClientVisualizer(analysis_results)
        else:
            raise ValueError(f"Type d'analyse inconnu: {analysis_type}")






if __name__ == "__main__":
    # Données factices pour tester https://sharemycode.fr/nhr
    fake_client_results = {
        "client_categories": {"petits_acheteurs": 50, "moyens_acheteurs": 30, "gros_acheteurs": 20},
        "oldest_inactive_clients": {"2023-01-15": 10, "2023-02-10": 5},
    }
    # Création des visualiseurs via la factory
    #transaction_viz = VisualizerFactory.get_visualizer(data_transaction,
                                                       #"transactions")
    client_viz = VisualizerFactory.get_visualizer(fake_client_results,
                                                       "clients")
    #client_viz.plot("client_distribution")
    client_viz.generate_pdf("clients_report.pdf")

# Statistiques des logs
from collections import Counter
import re
from datapulse91.processing.file_loader import load_file


def analyze_server_logs(log_path):
    """
    Analsye les logs serveur : distribution des codes HTTP, IPs actives et pics de trafic
    :param log_path:str chemin du fichier logs
    :return: dict - dictionnaire contenant les statistiques (total_requests, http_code_distribution, most_active_ips, traffic_by_hour)
    """

    http_codes = Counter()
    ip_addresses = Counter()
    traffic_by_hour = Counter()

    for line in load_file(log_path): # Lecture STREAM
        # Extraction du code HTTP (3 premiers chiffres trouvés)
        match_http = re.search(r"\b(\d{3})\b", line)
        if match_http:
            http_codes[match_http.group(1)] += 1

        # Extraction des adresses IP
        match_ip = re.search(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", line)
        if match_ip:
            ip_addresses[match_ip.group(0)] += 1

        match_time = re.search(r"\b(\d{2}):\d{2}:\d{2}\b", line)
        if match_time:
            traffic_by_hour[match_time.group(1)] += 1

    sorted_traffic_by_hour= dict(sorted(traffic_by_hour.items(), key=lambda x: int(x[0])))

    return {
        "total_requests": sum(http_codes.values()),
        "http_code_distribution" : dict(http_codes),
        "most_active_ips" : dict(ip_addresses.most_common(5)),
        "traffic_by_hour" : sorted_traffic_by_hour
    }

if __name__ == "__main__":
    print(analyze_server_logs("../../../data/server_logs.txt"))


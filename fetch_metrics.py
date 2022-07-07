import requests

from typing import List, Dict, Any


def fetch_brukernotifkasjoner_metrics(url: str, token: str) -> List[Dict[str, Any]]:
    headers = {"Authentication": token}

    resp = requests.get(url=url, headers=headers)
    resp.raise_for_status()

    return resp.json()

import allure
import requests
from requests import Response


class YandexSearchAPI:
    def __init__(self, base_url: str):
        self.base_url = base_url

    @allure.step(
        "Поиска по запросу '{text}' в локации ({longitude}, {latitude})"
    )
    def search(self, text: str, longitude: float, latitude: float) -> Response:
        payload = {
            "text": text,
            "filters": [],
            "location": {
                "longitude": longitude,
                "latitude": latitude,
            },
        }
        return requests.post(self.base_url, json=payload)

import requests

class API:
    def __init__(self, apiURL) -> None:
        self.url = apiURL
        pass

    def post(self, dados):
        try:
            req = requests.post(self.url, json = dados)
        except requests.ConnectionError as e:
            pass
        return req.status_code
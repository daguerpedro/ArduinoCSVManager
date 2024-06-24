import requests

class API:
    def __init__(self, apiURL) -> None:
        self.url = apiURL
        pass

    def post(self, dados):
        try:
            req = requests.post(self.url, json = dados)
        except Exception as e:
            print(f"[API] ${self.url} erro: ${e}")
            pass
        return req.status_code
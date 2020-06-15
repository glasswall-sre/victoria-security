import requests

class VictoriaIF:
    @staticmethod
    def call_victoria(shlex, secrets):
        url = secrets["VICTORIA_URL"]
        data = {
            'args': shlex
        }
        r = requests.post(url, json=data)
        return {
            'statusCode' : r.status_code,
            'body': r.json()
        }
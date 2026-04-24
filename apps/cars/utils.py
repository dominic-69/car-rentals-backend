import requests

def call_fastapi_price(data):
    try:
        res = requests.post(
            "http://127.0.0.1:8001/predict-price",
            json=data
        )
        return res.json()
    except Exception as e:
        return None
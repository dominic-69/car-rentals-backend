import requests
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Query(BaseModel):
    message: str


@app.post("/ai/chat/")
def ai_chat(data: Query):
    msg = data.message.lower()

    # 🔥 Extract price
    if "5 lakh" in msg:
        max_price = 500000
    elif "3 lakh" in msg:
        max_price = 300000
    else:
        return {"reply": "Please specify budget "}

    # 🔥 Call Django API
    try:
        res = requests.get(
            f"http://127.0.0.1:8000/api/cars/search/?max_price={max_price}"
        )
        cars = res.json()

        if not cars:
            return {"reply": "No cars found 😔"}

        # format response
        result = "Here are cars:\n"
        for car in cars[:5]:
            result += f"{car['title']} - ₹{car['price']}\n"

        return {"reply": result}

    except Exception as e:
        return {"reply": "Server error 😔"}
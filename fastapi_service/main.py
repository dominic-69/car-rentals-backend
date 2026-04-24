from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ✅ FIXED CORS (IMPORTANT)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],  # ✅ DO NOT use "*" with credentials
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ CHATBOT ROUTE
@app.post("/chatbot")
async def chatbot(data: dict):
    message = data.get("message", "").lower()

    if "cheap" in message:
        return {"reply": "Try Alto, Swift, i10 🚗"}
    elif "suv" in message:
        return {"reply": "Check Creta, Nexon, XUV300 🚙"}
    elif "car" in message:
        return {"reply": "We have SUV, Sedan, Hatchback 🚗"}
    else:
        return {"reply": "Tell me your budget 😊"}
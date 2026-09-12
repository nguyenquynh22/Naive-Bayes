from fastapi import FastAPI, HTTPException
import httpx

app = FastAPI(
    title="Used Car Backend API",
    description="Backend gateway forwarding prediction requests to the AI service",
    version="1.0.0",
)

AI_SERVICE_URL = "http://ai_service:8000"


@app.get("/")
def home():
    return {"status": "online", "service": "backend"}


@app.get("/health")
async def health():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{AI_SERVICE_URL}/", timeout=5.0)
            response.raise_for_status()
        return {"status": "online", "service": "backend", "ai_service": "online"}
    except httpx.HTTPError as error:
        raise HTTPException(status_code=503, detail=f"AI service unavailable: {error}") from error


@app.post("/predict")
async def predict(payload: dict):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{AI_SERVICE_URL}/predict",
                json=payload,
                timeout=30.0,
            )
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as error:
        detail = error.response.text or "AI service returned an error"
        raise HTTPException(status_code=error.response.status_code, detail=detail) from error
    except httpx.HTTPError as error:
        raise HTTPException(status_code=503, detail=f"AI service unavailable: {error}") from error

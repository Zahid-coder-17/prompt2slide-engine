from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import base64
from io import BytesIO

from app.image_engine import generate_image

app = FastAPI(title="Tazkirah Image Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ImageRequest(BaseModel):
    prompt: str
    mode: str = "default"
    seed: Optional[int] = None

    class Config:
        extra = "ignore"

@app.post("/generate-image")
def generate(req: ImageRequest):
    try:
        image = generate_image(
            user_prompt=req.prompt,
            mode=req.mode,
            seed=req.seed
        )

        buffer = BytesIO()
        image.save(buffer, format="PNG")
        img_b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

        return {
            "image_base64": img_b64
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health():
    return {"status": "ok"}

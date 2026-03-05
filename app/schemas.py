from pydantic import BaseModel
from typing import Optional

class ImageRequest(BaseModel):
    prompt: str
    mode: str = "default"
    seed: int | None = None

    class Config:
        extra = "ignore"

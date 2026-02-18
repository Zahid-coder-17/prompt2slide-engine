
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uuid
import os
import json

# 🔹 Your LLM function
from app import ask

# 🔹 Your image engine
from app.image_engine import generate_image

# 🔹 PPT generator
from ppt_generator import create_presentation


app = FastAPI(title="Prompt2Slide API")


# ============================================
# 📥 Request Schema
# ============================================

class SlideRequest(BaseModel):
    prompt: str
    slides: int = 3
    theme: str = "modern"


# ============================================
# 🧠 Helper: Extract Slides JSON Safely
# ============================================

def extract_slides_json(raw_text: str):
    """
    Extract JSON block starting from {"slides": ...}
    even if model prints extra text.
    """

    start = raw_text.find('{"slides"')
    if start == -1:
        raise ValueError("No slides JSON found in model output")

    brace_count = 0
    json_block = ""

    for char in raw_text[start:]:
        json_block += char
        if char == "{":
            brace_count += 1
        elif char == "}":
            brace_count -= 1
            if brace_count == 0:
                break

    return json.loads(json_block)


# ============================================
# 🚀 Main Endpoint
# ============================================

@app.post("/generate-slide")
def generate_slide(req: SlideRequest):

    try:
        # 1️⃣ Generate slides JSON from LLM
        slides_raw = ask(req.prompt, req.slides)

        slides_data = extract_slides_json(slides_raw)
        slides = slides_data["slides"]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM error: {str(e)}")

    try:
        # 2️⃣ Generate images
        os.makedirs("generated_images", exist_ok=True)

        for slide in slides:
            img = generate_image(
                slide["image_prompt"],
                mode="education"
            )

            img_path = f"generated_images/slide_{slide['slide_number']}.png"
            img.save(img_path)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image generation error: {str(e)}")

    try:
        # 3️⃣ Create PPT
        file_id = str(uuid.uuid4())
        ppt_name = f"{file_id}.pptx"

        create_presentation(
            slides=slides,
            theme=req.theme,
            output_file=ppt_name
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PPT generation error: {str(e)}")

    # 4️⃣ Return File
    return FileResponse(
        path=ppt_name,
        media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        filename="presentation.pptx"
    )

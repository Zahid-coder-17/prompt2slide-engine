import sys
from pathlib import Path

# add project root to PYTHONPATH
sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.image_engine import generate_image

img = generate_image(
    user_prompt="A modern classroom explaining machine learning concepts",
    mode="education",
    seed=42
)

img.save("outputs/test_edu.png")
print("Saved outputs/test_edu.png")

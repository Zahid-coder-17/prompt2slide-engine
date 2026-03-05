import sys
import os
import json
from app import ask
from app.image_engine import generate_image
from ppt_generator import create_presentation

def test_full_pipeline():
    prompt = "Artificial Intelligence concepts"
    num_slides = 1
    
    print(f"--- 1. Generating Slide JSON for: '{prompt}' ---")
    try:
        raw_response = ask(prompt, num_slides)
        print("Raw response from model:")
        print(raw_response)
        
        # Simple extraction logic from prompt2slide_api.py
        start = raw_response.find('{"slides"')
        if start == -1:
             print("❌ Error: Could not find JSON in model response.")
             return
             
        brace_count = 0
        json_block = ""
        for char in raw_response[start:]:
            json_block += char
            if char == "{": brace_count += 1
            elif char == "}": brace_count -= 1
            if brace_count == 0: break
            
        slides_data = json.loads(json_block)
        slides = slides_data["slides"]
        print("✅ Successfully parsed slides JSON.")
    except Exception as e:
        print(f"❌ LLM Error: {e}")
        return

    print(f"\n--- 2. Generating {len(slides)} Images ---")
    os.makedirs("generated_images", exist_ok=True)
    try:
        for slide in slides:
            print(f"Generating image for slide {slide['slide_number']}: {slide['image_prompt']}")
            img = generate_image(slide["image_prompt"], mode="education")
            img_path = f"generated_images/slide_{slide['slide_number']}.png"
            img.save(img_path)
            print(f"✅ Saved: {img_path}")
    except Exception as e:
        print(f"❌ Image Gen Error: {e}")
        # We can continue if images fail, ppt_generator handles missing images

    print("\n--- 3. Creating PowerPoint ---")
    try:
        output_file = "test_output.pptx"
        create_presentation(slides=slides, theme="modern", output_file=output_file)
        print(f"✅ Success! PowerPoint saved as: {os.path.abspath(output_file)}")
    except Exception as e:
        print(f"❌ PPT Error: {e}")

if __name__ == "__main__":
    # Ensure we can find the modules
    sys.path.append(os.getcwd())
    test_full_pipeline()

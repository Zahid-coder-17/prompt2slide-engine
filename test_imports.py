import sys
import os

# Ensure the root is in PYTHONPATH
sys.path.append(os.getcwd())

try:
    print("Testing imports...")
    from app import ask
    print("✅ Successfully imported 'ask' from 'app'")
    
    from app.image_engine import generate_image
    print("✅ Successfully imported 'generate_image' from 'app.image_engine'")
    
    from ppt_generator import create_presentation
    print("✅ Successfully imported 'create_presentation' from 'ppt_generator'")
    
    print("\nAll core components imported successfully!")
except Exception as e:
    print(f"❌ Import failed: {str(e)}")
    import traceback
    traceback.print_exc()

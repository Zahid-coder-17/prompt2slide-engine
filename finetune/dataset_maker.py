import json
import os

def create_synthetic_data():
    # We will create a small sample of training data specifically for the slide format
    # This helps the model follow the JSON structure perfectly and use the correct style
    
    data = [
        {
            "instruction": "Create a slide presentation about the pillars of Salah.",
            "context": "The Pillars of Salah (Arkan al-Salah) are the essential parts of the prayer that must be performed for it to be valid. There are 14 pillars including: 1. Standing if able, 2. Takbirat al-Ihram, 3. Reciting Al-Fatihah, 4. Ruku', 5. Rising from Ruku', 6. Prostration on seven bones, 7. Rising from prostration...",
            "response": {
                "slides": [
                    {
                        "slide_number": 1,
                        "title": "Introduction to Pillars of Salah",
                        "bullet_points": [
                            "Essential components of the prayer",
                            "Must be performed for the prayer to be valid",
                            "Total of 14 pillars in the prayer sequence"
                        ],
                        "image_prompt": "A serene educational illustration showing a sequence of prayer positions with numbers 1 to 14 clearly visible."
                    },
                    {
                        "slide_number": 2,
                        "title": "Initial Pillars",
                        "bullet_points": [
                            "Standing (Qiyam) if physically able",
                            "Takbirat al-Ihram: The opening 'Allahu Akbar'",
                            "Reciting Surah Al-Fatihah in every unit"
                        ],
                        "image_prompt": "A diagram of a person standing in prayer with focus on the opening takbir gesture."
                    }
                ]
            }
        },
        {
            "instruction": "Create a slide presentation about the basics of Machine Learning.",
            "context": "Machine learning (ML) is a field of study in artificial intelligence concerned with the development and study of statistical algorithms that can learn from data and generalize to unseen data. Key concepts include Training Data, Features, Labels, and Models. Types of ML include Supervised, Unsupervised, and Reinforcement Learning.",
            "response": {
                "slides": [
                    {
                        "slide_number": 1,
                        "title": "What is Machine Learning?",
                        "bullet_points": [
                            "A subset of Artificial Intelligence",
                            "Algorithms that learn from statistical patterns",
                            "Ability to generalize to new, unseen data"
                        ],
                        "image_prompt": "A modern digital illustration showing data points transforming into a predictive graph."
                    },
                    {
                        "slide_number": 2,
                        "title": "Core Components",
                        "bullet_points": [
                            "Features: The input variables used for prediction",
                            "Labels: The target output we want to predict",
                            "Model: The mathematical representation of the patterns"
                        ],
                        "image_prompt": "Infographic showing columns of data (features) pointing towards a result box (label)."
                    }
                ]
            }
        }
    ]
    
    output_path = "finetune/training_data.jsonl"
    with open(output_path, "w", encoding="utf-8") as f:
        for entry in data:
            # Format according to Phi-3 chat template style
            prompt = f"<|user|>\nInstruction: {entry['instruction']}\nContext: {entry['context']}<|end|>\n<|assistant|>\n{json.dumps(entry['response'])}<|end|>"
            f.write(json.dumps({"text": prompt}) + "\n")
            
    print(f"✅ Generated synthetic training data at {output_path}")

if __name__ == "__main__":
    create_synthetic_data()

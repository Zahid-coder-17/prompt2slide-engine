import os
import torch
from datasets import load_dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling
)
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training

def train():
    model_id = "microsoft/phi-3-mini-4k-instruct"
    dataset_path = "finetune/training_data.jsonl"
    output_dir = "finetune/phi3-lora-output"
    
    print(f"Loading tokenizer and model: {model_id}")
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    tokenizer.pad_token = tokenizer.eos_token
    
    device = "cuda" if torch.cuda.is_available() else "cpu"
    
    # Load model with specific config based on hardware
    if device == "cuda":
        # QLoRA (if bitsandbytes is available) or just load in 16-bit
        model = AutoModelForCausalLM.from_pretrained(
            model_id,
            trust_remote_code=True,
            torch_dtype=torch.float16,
            device_map="auto"
        )
    else:
        print("⚠️ No GPU detected. Training on CPU will be extremely slow.")
        model = AutoModelForCausalLM.from_pretrained(
            model_id,
            trust_remote_code=True,
            torch_dtype=torch.float32,
            device_map="cpu"
        )

    # LoRA Config
    lora_config = LoraConfig(
        r=8,
        lora_alpha=16,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM"
    )

    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()

    # Load dataset
    dataset = load_dataset("json", data_files=dataset_path, split="train")
    
    def tokenize_function(examples):
        return tokenizer(examples["text"], padding="max_length", truncation=True, max_length=512)

    tokenized_dataset = dataset.map(tokenize_function, batched=True)

    # Training Arguments
    training_args = TrainingArguments(
        output_dir=output_dir,
        per_device_train_batch_size=1,
        gradient_accumulation_steps=4,
        learning_rate=2e-4,
        logging_steps=1,
        num_train_epochs=1, # Just 1 epoch for the demonstration
        save_steps=10,
        evaluation_strategy="no",
        fp16=(device == "cuda"),
        report_to="none"
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_dataset,
        data_collator=DataCollatorForLanguageModeling(tokenizer, mlm=False),
    )

    print("Starting training...")
    trainer.train()
    
    # Save the adapter
    model.save_pretrained(os.path.join(output_dir, "final_adapter"))
    print(f"✅ Training complete. Adapter saved to {output_dir}/final_adapter")

if __name__ == "__main__":
    if not os.path.exists("finetune/training_data.jsonl"):
        print("❌ Dataset not found. Run dataset_maker.py first.")
    else:
        train()

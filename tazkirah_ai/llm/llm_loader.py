from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
import torch

MODEL_PATH = "microsoft/phi-3-mini-4k-instruct"

# 8-bit config
bnb_config = BitsAndBytesConfig(
    load_in_8bit=True
)

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)

model = AutoModelForCausalLM.from_pretrained(
    MODEL_PATH,
    quantization_config=bnb_config,
    device_map="auto",
    torch_dtype=torch.float16,
    low_cpu_mem_usage=True
)


def generate(prompt, max_new_tokens=554):

    messages = [
        {"role": "user", "content": prompt}
    ]

    # Use proper Phi-3 chat template
    inputs = tokenizer.apply_chat_template(
        messages,
        tokenize=True,
        add_generation_prompt=True,
        return_tensors="pt"
    )

    inputs = {k: v.to(model.device) for k, v in inputs.items()}

    input_length = inputs["input_ids"].shape[1]

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            temperature=0.2,
            do_sample=True
        )

    # 🔥 Decode ONLY newly generated tokens
    generated_tokens = outputs[0][input_length:]

    decoded = tokenizer.decode(generated_tokens, skip_special_tokens=True)

    # 🔥 Extract clean JSON starting from {"slides"
    start = decoded.find('{"slides"')
    if start != -1:
        decoded = decoded[start:]

    return decoded.strip()

from guardrails import apply_guardrails
from diffusers import StableDiffusionPipeline
import torch

user_prompt = "A serene landscape with mountains and a river at sunset, in the style of a digital painting."

result = apply_guardrails(user_prompt, mode="reject")

if not result["allowed"]:
    print("Rejected:", result["reason"])
    exit()

pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch.float16
).to("cuda")

pipe.load_lora_weights("C:/lora_output", weight_name="edu_islamic_lora_v1.safetensors")
pipe.fuse_lora(lora_scale=0.6)

image = pipe(
    result["prompt"],
    negative_prompt=result["negative_prompt"],
    num_inference_steps=25,
    guidance_scale=7
).images[0]

image.save("output.png")

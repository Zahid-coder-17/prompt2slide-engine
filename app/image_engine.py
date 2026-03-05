import torch
from diffusers import (
    StableDiffusionPipeline,
    DPMSolverMultistepScheduler
)

# ------------------------
# CONFIG
# ------------------------

MODEL_ID = "runwayml/stable-diffusion-v1-5"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

_pipe = None
_default_scheduler_config = None


# ------------------------
# PIPELINE LOADER (singleton)
# ------------------------

def load_pipeline():
    """
    Load SD pipeline only once (singleton).
    Safe for FastAPI.
    """
    global _pipe, _default_scheduler_config

    if _pipe is not None:
        return _pipe

    pipe = StableDiffusionPipeline.from_pretrained(
        MODEL_ID,
        torch_dtype=torch.float16 if DEVICE == "cuda" else torch.float32,
        safety_checker=None
    ).to(DEVICE)

    # Performance / VRAM optimizations
    pipe.enable_attention_slicing()
    pipe.enable_vae_slicing()

    # Optional speedups (enable only if available)
    try:
        pipe.enable_xformers_memory_efficient_attention()
    except Exception:
        pass

    # Torch compile (PyTorch 2.x)
    try:
        pipe.unet = torch.compile(pipe.unet, mode="reduce-overhead")
    except Exception:
        pass

    _default_scheduler_config = pipe.scheduler.config
    _pipe = pipe

    return _pipe


# ------------------------
# MODE CONFIGURATION
# ------------------------

def get_mode_config(mode: str):
    """
    Centralized generation policy
    """

    if mode == "cinematic":
        return {
            "scheduler": "dpm",
            "steps": 30,
            "cfg": 6.5,
            "width": 768,
            "height": 432,
            "prompt_prefix": (
                "cinematic wide-angle shot, professional film lighting, "
                "soft global illumination, volumetric light rays, "
                "shallow depth of field, film still, color graded, HDR, "
            )
        }

    elif mode == "education":
        return {
            "scheduler": "default",
            "steps": 25,
            "cfg": 8.0,
            "width": 512,
            "height": 512,
            "prompt_prefix": (
                "clear educational illustration, simple composition, "
                "clean background, informative visual, "
            )
        }

    elif mode == "architecture":
        return {
            "scheduler": "dpm",
            "steps": 28,
            "cfg": 7.5,
            "width": 640,
            "height": 512,
            "prompt_prefix": (
                "architectural visualization, symmetrical composition, "
                "realistic lighting, high detail, "
            )
        }

    else:  # default
        return {
            "scheduler": "default",
            "steps": 25,
            "cfg": 7.5,
            "width": 512,
            "height": 512,
            "prompt_prefix": ""
        }


# ------------------------
# IMAGE GENERATION
# ------------------------

def generate_image(
    user_prompt: str,
    mode: str = "default",
    seed: int | None = None,
):
    """
    Generate a single image from text.
    """

    pipe = load_pipeline()
    config = get_mode_config(mode)

    # Scheduler (thread-safe)
    if config["scheduler"] == "dpm":
        scheduler = DPMSolverMultistepScheduler.from_config(
            _default_scheduler_config
        )
    else:
        scheduler = pipe.scheduler

    # Seed control
    generator = None
    if seed is not None:
        generator = torch.Generator(device=DEVICE).manual_seed(seed)

    # Final prompt
    final_prompt = f"{config['prompt_prefix']}{user_prompt}"

    # Inference
    with torch.no_grad():
        image = pipe(
            final_prompt,
            num_inference_steps=config["steps"],
            guidance_scale=config["cfg"],
            width=config["width"],
            height=config["height"],
            generator=generator,
            scheduler=scheduler
        ).images[0]

    return image

    # in app/image_engine.py
_PIPE = None

def get_pipeline():
    global _PIPE
    if _PIPE is None:
        _PIPE = load_pipeline()
        _ = _PIPE("warmup", num_inference_steps=1)
    return _PIPE

def apply_lora(pipe, lora_path: str | None):
    global _CURRENT_LORA

    # If no LoRA requested, unload existing
    if lora_path is None:
        if _CURRENT_LORA is not None:
            pipe.unload_lora_weights()
            _CURRENT_LORA = None
        return

    # If same LoRA already loaded, do nothing
    if _CURRENT_LORA == lora_path:
        return

    # Switch LoRA
    if _CURRENT_LORA is not None:
        pipe.unload_lora_weights()

    pipe.load_lora_weights(lora_path)
    _CURRENT_LORA = lora_path

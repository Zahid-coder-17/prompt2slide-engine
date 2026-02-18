# guardrails.py

import re

# -----------------------------
# CONFIG
# -----------------------------

# Hard-blocked keywords (non-human / non-Islamic)
BLOCKED_KEYWORDS = [
    "angel", "angels", "jinn", "djinn", "demon", "devil", "spirit", "ghost",
    "god", "gods", "deity", "idol", "statue", "worship",
    "myth", "mythical", "mythology", "fantasy", "celestial",
    "alien", "extraterrestrial",
    "humanoid animal", "animal humanoid",
    "robot with face", "android", "cyborg",
    "magic", "sorcery", "occult"
]

# System prompt (ALWAYS injected)
SYSTEM_PROMPT = (
    "You are an educational image generator strictly aligned with Islamic values. "
    "Generate only real human beings and real-world environments. "
    "Do not generate non-human beings, angels, jinn, demons, gods, idols, statues of worship, "
    "fantasy creatures, or mythological entities. "
    "Images must be modest, respectful, realistic, and suitable for Islamic education."
)

# Negative prompt (ALWAYS appended)
NEGATIVE_PROMPT = (
    "non-human, angel, jinn, demon, god, deity, idol, statue, mythological creature, fantasy being, "
    "alien, robot humanoid, cyborg, wings, halo, divine face, glowing being, "
    "magic, sorcery, occult, "
    "nudity, revealing clothing, sexualized body, "
    "violence, blood, gore, "
    "text, watermark, logo"
)

# -----------------------------
# CORE FUNCTIONS
# -----------------------------

def normalize(text: str) -> str:
    """Lowercase + remove extra symbols for safer matching"""
    return re.sub(r"[^a-zA-Z0-9\s]", "", text.lower())


def contains_blocked_content(prompt: str) -> bool:
    """Check if prompt contains forbidden concepts"""
    clean = normalize(prompt)
    return any(keyword in clean for keyword in BLOCKED_KEYWORDS)


def rewrite_prompt(prompt: str) -> str:
    """
    Rewrite ambiguous prompts into allowed abstract representations.
    Used ONLY if you choose rewrite instead of reject.
    """
    return (
        "educational abstract illustration using light, geometry, and symbolism, "
        "no living beings, no faces, no figures, "
        "clean, minimal, respectful, Islamic educational style"
    )


def apply_guardrails(
    user_prompt: str,
    mode: str = "reject"  # "reject" or "rewrite"
):
    """
    Main guardrail entry point.
    Returns dict with safe prompt config OR error.
    """

    if contains_blocked_content(user_prompt):
        if mode == "reject":
            return {
                "allowed": False,
                "reason": "Non-human or non-Islamic content is not allowed."
            }

        elif mode == "rewrite":
            safe_prompt = rewrite_prompt(user_prompt)
        else:
            raise ValueError("mode must be 'reject' or 'rewrite'")

    else:
        safe_prompt = user_prompt

    return {
        "allowed": True,
        "system_prompt": SYSTEM_PROMPT,
        "prompt": safe_prompt,
        "negative_prompt": NEGATIVE_PROMPT
    }

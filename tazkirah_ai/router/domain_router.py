def route_domain(query: str) -> str:
    q = query.lower()

    islamic_keywords = [
        "quran", "ayah","Prayer", "salah", "namaz", "niyyah", "wudu",
        "zakat","islam", "fasting", "ramadan", "hadith", "fiqh", "dua"
    ]

    ml_keywords = [
        "machine learning", "ml", "ai", "model", "loss",
        "gradient", "neural", "training", "optimizer", "dataset"
    ]

    if any(word in q for word in islamic_keywords):
        return "islamic"

    if any(word in q for word in ml_keywords):
        return "ml"

    # SAFE DEFAULT
    return "ml"

import os
from .rag.retrieve import retrieve
from .llm.llm_loader import generate
from .router.domain_router import route_domain


def ask(question, num_slides=5):
    # Step 1: Route domain
    domain = route_domain(question)

    # Step 2: Retrieve context
    context = retrieve(question, domain)

    # Step 3: Load base prompt template
    prompt_path = os.path.join(os.path.dirname(__file__), "prompts", "base_prompt.txt")
    with open(prompt_path) as f:
        template = f.read()

    # Step 4: Format final prompt
    prompt = template.format(
        context=context,
        question=question,
        num_slides=num_slides
    )

    print(f"\n🔍 Routed to domain: {domain.upper()}")
    print(f"📊 Generating {num_slides} slides...\n")

    # Step 5: Generate response
    response = generate(prompt)

    # Clean possible assistant prefix (Phi models sometimes echo prompt)
    if "<|assistant|>" in response:
        response = response.split("<|assistant|>")[-1].strip()

    if not response.strip():
        print("⚠️ Model returned empty response.")
        return None

    print(response)
    return response


if __name__ == "__main__":
    question = input("Enter your question: ")
    slides = int(input("Enter number of slides: "))
    ask(question, slides)


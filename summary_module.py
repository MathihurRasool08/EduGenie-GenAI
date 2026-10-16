from gemini_client import generate_text

def summarize_text(text: str) -> str:
    prompt = f"""Summarize the following educational passage for quick revision. Preserve the important facts, definitions, relationships, and conclusions. Use clear headings and concise bullet points where useful. Do not add information that is not present.\n\nPASSAGE:\n{text}"""
    return generate_text(prompt)

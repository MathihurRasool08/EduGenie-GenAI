from gemini_client import generate_text

def answer_question(question: str, context: str = "") -> str:
    context_block = f"\nReference context:\n{context}" if context else ""
    prompt = f"""You are EduGenie, an accurate academic tutor. Answer the student's question clearly and directly.{context_block}\n\nQuestion: {question}\n\nRules:\n- Give the answer first.\n- Explain the reasoning at an appropriate student level.\n- If the question is ambiguous, state the assumption.\n- Do not invent citations or sources.\n- If you are uncertain, say so rather than fabricating facts."""
    return generate_text(prompt)

from .ai_chat import AI


def summarize_website(text: str) -> str:
    """
    Function to summarize the text using a specific AI model

    Args:
        text (str): The text to be summarized
        model (str): The model to use for summarization

    Returns:
        str: The summarized text
    """

    prompt = f"Create a knowledge base of the tools, templates and references, in 300 words or less for the following website content: {text[:3000]}"
    ai_chat = AI("")
    summary = ai_chat.chat(prompt)

    return summary

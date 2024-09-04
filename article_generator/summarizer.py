from .ai_chat import AI
from logging_setup import setup_logger

log = setup_logger(__name__)


def summarize_website(text: str) -> str:
    """
    Function to summarize the text using a specific AI model

    Args:
        text (str): The text to be summarized
        model (str): The model to use for summarization

    Returns:
        str: The summarized text
    """

    log.info("Summarizing the website content...")

    prompt = f"Create a knowledge base of the tools, templates and references, in 300 words or less for the following website content: {text[:3000]}"
    try:
        ai_chat = AI("")
    except Exception as e:
        log.error(f"Error initializing AI Chat: {e}")
        return "", f"Error initializing AI Chat"

    summary, summary_error = ai_chat.chat(prompt)

    if summary_error:
        log.error(f"Error summarizing website content: {summary_error}")
        return "", f"Error summarizing website content:\n\n{summary_error}"

    return summary, None

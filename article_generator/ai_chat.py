import time
from openai import (
    OpenAI,
    RateLimitError as OpenAIRateLimitError,
    APIConnectionError as OpenAIAPIConnectionError,
    APIError as OpenAIAPIError,
)
from anthropic import (
    Anthropic,
    RateLimitError as ClaudeRateLimitError,
    APIConnectionError as ClaudeAPIConnectionError,
    APIError as ClaudeAPIError,
)
from utils.config_manager import ConfigManager
from logging_setup import setup_logger

log = setup_logger(__name__)


class AI:
    def __init__(self, system_prompt: str):

        log.info("Initializing AI Chat...")

        # Initialize the config manager
        self.config_manager = ConfigManager()

        # Load the param_config.json file
        self.ai_provider = self.config_manager.load_params()["ai_provider"]

        if self.ai_provider == "openai":
            log.debug("AI provider: OpenAI")
            self.openai_init(system_prompt)
        elif self.ai_provider == "claude":
            log.debug("AI provider: Claude")
            self.claude_init(system_prompt)
        else:
            raise ValueError("Invalid AI provider")

    def openai_init(self, system_prompt: str):
        log.info("Initializing OpenAI Chat...")

        config = self.config_manager.load_params()["openai_params"]
        config = config["openai_params"]
        self.api_key = config["api_key"]
        self.max_tokens = config["max_tokens"]
        self.temperature = config["temperature"]
        self.max_retries = config["max_retries"]
        self.default_model = config["default_model"]

        # Initialize the conversation
        self.conversation = [
            {"role": "system", "content": system_prompt},
        ]

        # Setup the Open AI client
        try:
            self.client = OpenAI(api_key=self.api_key)
        except Exception as e:
            log.error(f"Error initializing OpenAI client: {e}")
            raise

    def openai_chat(
        self,
        message: str,
        model: str = None,
        temperature: float = None,
        retry_delay: int = 5,
    ) -> tuple[str, str | None]:
        """
        Function to chat with OpenAI

        Args:
            message (str): The message to send to OpenAI
            model (str): The model to use for the response
            temperature (float): The temperature for the response
            retry_delay (int): The delay between retries

        Returns:
            response (str): The response from OpenAI
            error (str | None): The error message if any
        """
        # Append the message to the messages list
        self.conversation.append({"role": "user", "content": message})

        # Initialize the attempt counter
        attempt = 0
        attempt_success = False

        # Loop to retry the request if it fails
        while attempt < self.max_retries and not attempt_success:
            attempt += 1

            # Get the response from OpenAI
            try:
                log.info("Sending message to OpenAI...")
                response = self.client.chat.completions.create(
                    messages=self.conversation,
                    max_tokens=self.max_tokens,
                    temperature=temperature if temperature else self.temperature,
                    model=model if model else self.default_model,
                    response_format={"type": "text"},
                )
                attempt_success = True
                log.info("Got response from OpenAI")

            except OpenAIRateLimitError as e:
                # Handle rate limit error with exponential backoff

                if attempt == self.max_retries:
                    log.error("Max retries reached for rate limit.")
                    return "", "Max retries reached for rate limit."

                log.warning("Rate limit error. Retrying...")
                delay = retry_delay * (2**attempt)
                time.sleep(delay)

            except OpenAIAPIConnectionError as e:
                # Handle API connection error

                if attempt == self.max_retries:
                    log.error("Max retries reached for connection errors.")
                    return "", "Max retries reached for connection errors."

                log.warning("API connection error. Retrying...")
                delay = retry_delay * (2**attempt)
                time.sleep(delay)

            except OpenAIAPIError as e:
                # Handle general API errors

                if attempt == self.max_retries:
                    log.error("Max retries reached for API errors.")
                    return (
                        "",
                        "Max retries reached for API errors. Please check that your OpenAI API key is correct.",
                    )

                log.warning("API error. Retrying...")
                log.debug(e)
                delay = retry_delay * (2**attempt)
                time.sleep(delay)

            except Exception as e:
                # Catch-all for any other exceptions
                log.error(f"Error sending message to OpenAI: {e}")

                return (
                    "",
                    "An unexpected error occurred while getting the response from OpenAI.",
                )

        # Get the content of the response
        content = response.choices[0].message.content

        # Append the response to the messages list
        self.conversation.append({"role": "assistant", "content": content})

        return content, None

    def claude_init(self, system_prompt):
        config = self.config_manager.load_params()["claude_params"]
        self.conversation = []
        self.api_key = config["api_key"]
        self.max_tokens = config["max_tokens"]
        self.temperature = config["temperature"]
        self.max_retries = config["max_retries"]
        self.default_model = config["default_model"]

        self.system = system_prompt

        # Setup the Claude client
        try:
            self.client = Anthropic(api_key=self.api_key)
        except Exception as e:
            log.error(f"Error initializing Claude client: {e}")
            raise

    def claude_chat(
        self,
        message: str,
        model: str = None,
        temperature: float = None,
        retry_delay: int = 5,
    ) -> tuple[str, str | None]:
        """
        Function to chat with Claude

        Args:
            message (str): The message to send to Claude
            model (str): The model to use for the response
            temperature (float): The temperature for the response
            retry_delay (int): The delay between retries

        Returns:
            response (str): The response from Claude
            error (str | None): The error message if any
        """

        log.info("Sending message to Claude...")

        # Append the message to the messages list
        self.conversation.append({"role": "user", "content": message})

        # Initialize the attempt counter
        attempt = 0
        attempt_success = False

        # Loop to retry the request if it fails
        while attempt < self.max_retries and not attempt_success:
            attempt += 1

            # Get the response from OpenAI
            try:
                response = self.client.messages.create(
                    model=model if model else self.default_model,
                    max_tokens=self.max_tokens,
                    temperature=temperature if temperature else self.temperature,
                    system=self.system,
                    messages=self.conversation,
                )
                attempt_success = True

            except ClaudeRateLimitError as e:
                # Handle rate limit error with exponential backoff

                if attempt == self.max_retries:
                    log.error("Max retries reached for rate limit.")
                    return "", "Max retries reached for rate limit."

                log.warning("Rate limit error. Retrying...")
                delay = retry_delay * (2**attempt)
                time.sleep(delay)

            except ClaudeAPIConnectionError as e:
                # Handle API connection error

                if attempt == self.max_retries:
                    log.error("Max retries reached for connection errors.")
                    return "", "Max retries reached for connection errors."

                log.warning("API connection error. Retrying...")
                delay = retry_delay * (2**attempt)
                time.sleep(delay)

            except ClaudeAPIError as e:
                # Handle general API errors

                if attempt == self.max_retries:
                    log.error("Max retries reached for API errors.")
                    return (
                        "",
                        "Max retries reached for API errors. Claude might be overloaded. Please check that your Claude API key is correct.",
                    )

                log.warning("API error. Retrying...")
                log.debug(e)
                delay = retry_delay * (2**attempt)
                time.sleep(delay)

            except Exception as e:
                # Catch-all for any other exceptions

                log.error(f"Error sending message to Claude: {e}")
                return (
                    "",
                    "An unexpected error occurred while getting the response from Claude.",
                )

        # Get the content of the response
        content = response.content[0].text

        # Append the response to the messages list
        self.conversation.append({"role": "assistant", "content": content})

        return content, None

    def chat(
        self,
        message: str,
        model: str = None,
        temperature: float = None,
        retry_delay: int = 5,
    ) -> tuple[str, str | None]:
        """
        Function to chat with the AI provider

        Args:
            message (str): The message to send to the AI provider
            model (str): The model to use for the response
            temperature (float): The temperature for the response
            retry_delay (int): The delay between retries

        Returns:
            response (str): The response from the AI provider
            error (str | None): The error message if any
        """

        log.info("Sending AI message...")

        if self.ai_provider == "openai":
            response, error = self.openai_chat(
                message,
                model=model,
                temperature=temperature,
                retry_delay=retry_delay,
            )

            if error:
                log.error(f"Error sending message to OpenAI: {error}")
                return "", f"Error sending message to OpenAI:\n\n{error}"

            return response, None

        elif self.ai_provider == "claude":
            response, error = self.claude_chat(
                message, model=model, temperature=temperature, retry_delay=retry_delay
            )

            if error:
                log.error(f"Error sending message to Claude: {error}")
                return "", f"Error sending message to Claude:\n\n{error}"

            return response, None

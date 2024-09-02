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
from utils.config_loader import load_config


class AI:
    def __init__(self, system_prompt):

        # Load the param_config.json file
        self.ai_provider = load_config("param_config")["ai_provider"]

        if self.ai_provider == "openai":
            self.openai_init(system_prompt)
        elif self.ai_provider == "claude":
            self.claude_init(system_prompt)
        else:
            raise ValueError("Invalid AI provider")

    def openai_init(self, system_prompt: str):
        config = load_config("param_config")["openai_params"]
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
        self.client = OpenAI(api_key=self.api_key)

    def openai_chat(
        self,
        message: str,
        model: str = None,
        temperature: float = None,
        retry_delay: int = 5,
    ) -> str:
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
                response = self.client.chat.completions.create(
                    messages=self.conversation,
                    max_tokens=self.max_tokens,
                    temperature=temperature if temperature else self.temperature,
                    model=model if model else self.default_model,
                    response_format={"type": "text"},
                )
                attempt_success = True

            except OpenAIRateLimitError as e:
                # Handle rate limit error with exponential backoff

                if attempt == self.max_retries:
                    return "Max retries reached for rate limit."

                delay = retry_delay * (2**attempt)
                time.sleep(delay)

            except OpenAIAPIConnectionError as e:
                # Handle API connection error

                if attempt == self.max_retries:
                    return "Max retries reached for connection errors."

                delay = retry_delay * (2**attempt)
                time.sleep(delay)

            except OpenAIAPIError as e:
                # Handle general API errors

                if attempt == self.max_retries:
                    return "Max retries reached for API error."

                delay = retry_delay * (2**attempt)
                time.sleep(delay)

            except Exception as e:
                # Catch-all for any other exceptions
                raise

        # Get the content of the response
        content = response.choices[0].message.content

        # Append the response to the messages list
        self.conversation.append({"role": "assistant", "content": content})

        return content

    def claude_init(self, system_prompt):
        config = load_config("param_config")["claude_params"]
        self.conversation = []
        self.api_key = config["api_key"]
        self.max_tokens = config["max_tokens"]
        self.temperature = config["temperature"]
        self.max_retries = config["max_retries"]
        self.default_model = config["default_model"]

        self.system = system_prompt

        # Setup the Claude client
        self.client = Anthropic(api_key=self.api_key)

    def claude_chat(
        self,
        message: str,
        model: str = None,
        temperature: float = None,
        retry_delay: int = 5,
    ) -> str:
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
                    return "Max retries reached for rate limit."

                delay = retry_delay * (2**attempt)
                time.sleep(delay)

            except ClaudeAPIConnectionError as e:
                # Handle API connection error

                if attempt == self.max_retries:
                    return "Max retries reached for connection errors."

                delay = retry_delay * (2**attempt)
                time.sleep(delay)

            except ClaudeAPIError as e:
                # Handle general API errors

                if attempt == self.max_retries:
                    return "Max retries reached for API error."

                delay = retry_delay * (2**attempt)
                time.sleep(delay)

            except Exception as e:
                # Catch-all for any other exceptions
                raise

        # Get the content of the response
        content = response.content[0].text

        # Append the response to the messages list
        self.conversation.append({"role": "assistant", "content": content})

        return content

    def chat(
        self,
        message: str,
        model: str = None,
        temperature: float = None,
        retry_delay: int = 5,
    ) -> str:
        if self.ai_provider == "openai":
            response = self.openai_chat(
                message, model=model, temperature=temperature, retry_delay=retry_delay
            )
            return response
        elif self.ai_provider == "claude":
            response = self.claude_chat(
                message, model=model, temperature=temperature, retry_delay=retry_delay
            )
            return response

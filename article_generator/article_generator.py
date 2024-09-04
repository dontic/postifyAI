# article_generator.py

from article_generator.ai_chat import AI
from utils.config_loader import load_config
from article_generator import serp_api, content_fetcher, summarizer
from logging_setup import setup_logger

log = setup_logger(__name__)


class ArticleGenerator:
    def __init__(self):
        print("Initializing Article Generator...")

        # Load article_params from the param_config.json file
        self.article_params = load_config("param_config")["article_params"]
        self.language = self.article_params["language"]
        self.article_type = self.article_params["article_type"]
        self.expertise_field = self.article_params["expertise_field"]
        self.keyphrase = self.article_params["keyphrase"]
        self.product_name = self.article_params["product_name"]
        self.product_description = self.article_params["product_description"]
        self.product_url = self.article_params["product_url"]

        # Load the AI steps for the type of article
        self.ai_prompts = load_config("prompt_config")

        # Load the prompt config for the article type
        self.ai_prompts = self.ai_prompts[self.article_type]

        self.system_prompt = "\n".join(self.ai_prompts["system_prompt"])

        # Load the steps. Take into account that for each step, the prompt must be joined into a single string
        self.steps = [
            {
                "enhanced": step["enhanced"],
                "prompt": "\n".join(step["prompt"]),
            }
            for step in self.ai_prompts["steps"]
        ]

        print("Article Generator Initialized.")

    def generate(self) -> tuple[str, str | None]:
        log.info("Generating the article...")

        # Get the top urls from the search engine
        log.info(f"Getting top URLs for keyphrase: {self.keyphrase}")
        urls, serpapi_error = serp_api.get_google_search_top_urls(self.keyphrase)

        if serpapi_error:
            log.error(f"Error getting SERP URLs: {serpapi_error}")
            return "", f"Error getting SERP URLs:\n\n{serpapi_error}"

        # Get the content from the top urls
        log.info("Fetching content from the top URLs...")
        contents, content_fetching_error = content_fetcher.fetch_all_contents(urls)
        if content_fetching_error:
            log.error(f"Error fetching content: {content_fetching_error}")
            return "", f"Error fetching content:\n\n{content_fetching_error}"

        log.info(f"Fetched {len(contents)} contents")

        # Summarize each content
        log.info("Summarizing the content...")
        summaries = []

        for content in contents:
            summary, summary_error = summarizer.summarize_website(content)
            if summary_error:
                log.error(f"Error summarizing content: {summary_error}")
                return "", f"Error summarizing content:\n\n{summary_error}"
            summaries.append(summary)

        # Combine all the summaries into one summary
        log.info(
            f"Summarized {len(summaries)} contents, generating a combined summary..."
        )
        combined_content_summary = summarizer.summarize_website("\n".join(summaries))

        log.info("Content Summarized.")

        # Populate the system prompt with the variables
        log.info("Populating the system prompt...")
        formatted_system_prompt = self.system_prompt.format(
            language=self.language,
            expertise_field=self.expertise_field,
            keyphrase=self.keyphrase,
            product_name=self.product_name,
            product_description=self.product_description,
            product_url=self.product_url,
            combined_content_summary=combined_content_summary,
        )

        log.info("System Prompt populated.")

        # Initialize the AI chat
        log.info("Initializing AI Chat...")
        ai_chat = AI(formatted_system_prompt)
        log.info("AI Chat Initialized.")

        # Loop through the steps and generate the article
        full_article_list = []
        for step in self.steps:
            step_prompt = step["prompt"].format(
                language=self.language,
                expertise_field=self.expertise_field,
                keyphrase=self.keyphrase,
                product_name=self.product_name,
                product_description=self.product_description,
                product_url=self.product_url,
                combined_content_summary=combined_content_summary,
            )
            response = ai_chat.chat(step_prompt)
            full_article_list.append(response)

        # Combine the article parts into a single article
        full_article = "\n".join(full_article_list)

        return full_article, None

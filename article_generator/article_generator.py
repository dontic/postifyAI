# article_generator.py

from article_generator.ai_chat import AI
from utils.config_loader import load_config
from article_generator import serp_api, content_fetcher, summarizer


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

    def generate(self):
        print("Generating Article...")

        # Get the top urls from the search engine
        print(f"Getting top URLs for keyphrase: {self.keyphrase}")
        urls = serp_api.get_google_search_top_urls(self.keyphrase)
        print(f"Top URLs: {urls}")

        # Get the content from the top urls
        print("Fetching content from the top URLs...")
        contents = content_fetcher.fetch_all_contents(urls)
        print(f"Fetched {len(contents)} contents")

        # Summarize each content
        print("Summarizing the content...")
        summaries = [summarizer.summarize_website(content) for content in contents]

        # Combine all the summaries into one summary
        combined_content_summary = summarizer.summarize_website("\n".join(summaries))
        print(f"Combined Content Summary: {combined_content_summary}")

        # Populate the system prompt with the variables
        print("Populating the system prompt...")
        formatted_system_prompt = self.system_prompt.format(
            language=self.language,
            expertise_field=self.expertise_field,
            keyphrase=self.keyphrase,
            product_name=self.product_name,
            product_description=self.product_description,
            product_url=self.product_url,
            combined_content_summary=combined_content_summary,
        )
        print(formatted_system_prompt)

        # Initialize the AI chat
        print("Initializing AI Chat...")
        ai_chat = AI(formatted_system_prompt)
        print("AI Chat Initialized.")

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
            print(step_prompt)
            response = ai_chat.chat(step_prompt)
            full_article_list.append(response)
            print(response)

        # Combine the article parts into a single article
        full_article = "\n".join(full_article_list)

        return full_article

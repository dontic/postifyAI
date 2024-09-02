import serpapi
from utils.config_loader import load_config

# Load the param_config.json file
config = load_config("param_config")


def get_google_search_top_urls():
    serpapi_client = serpapi.Client(api_key=config["serp_params"]["api_key"])
    search_results = serpapi_client.search(
        q=config["article_params"]["keyphrase"],
        engine="google",
        gl=config["serp_params"]["country"],
    )
    organic_results = search_results.get("organic_results", [])
    urls = [
        result["link"]
        for result in organic_results[: config["serp_params"]["max_results"]]
    ]

    return urls

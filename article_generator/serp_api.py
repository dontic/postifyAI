import serpapi
from utils.config_loader import load_config

# Load the param_config.json file
serp_config = load_config("param_config")["serp_params"]


def get_google_search_top_urls(query):
    serpapi_client = serpapi.Client(api_key=serp_config["api_key"])
    search_results = serpapi_client.search(
        q=query,
        engine="google",
        gl=serp_config["country"],
    )
    organic_results = search_results.get("organic_results", [])
    urls = [result["link"] for result in organic_results[: serp_config["max_results"]]]

    return urls

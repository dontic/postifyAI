import serpapi
from serpapi import SerpApiError, HTTPConnectionError
from utils.config_loader import load_config

# Load the param_config.json file
serp_config = load_config("param_config")["serp_params"]


def get_google_search_top_urls(query: str) -> tuple[list[str], str | None]:
    # Initialize the error
    error = None

    # Initialize the serpapi client
    serpapi_client = serpapi.Client(api_key=serp_config["api_key"])

    # Try to get the search results
    try:
        search_results = serpapi_client.search(
            q=query,
            engine="google",
            gl=serp_config["country"],
        )
    except HTTPConnectionError:
        error = "Could not connect to the SerpApi server"
        return [], error
    except SerpApiError:
        error = "Client error, check that your Serp API key is correct"
        return [], error
    except:
        error = "An unexpected error ocurred, please fill an issue in https://github.com/dontic/SEOContentAI"
        return [], error

    organic_results = search_results.get("organic_results", [])
    urls = [result["link"] for result in organic_results[: serp_config["max_results"]]]

    return urls, None

import serpapi
from serpapi import SerpApiError, HTTPConnectionError
from utils.config_loader import load_config
from logging_setup import setup_logger

log = setup_logger(__name__)

# Load the param_config.json file
serp_config = load_config("param_config")["serp_params"]


def get_google_search_top_urls(query: str) -> tuple[list[str], str | None]:
    # Initialize the error
    error = None

    # Initialize the serpapi client
    log.debug("Initializing SerpApi client...")
    serpapi_client = serpapi.Client(api_key=serp_config["api_key"])

    # Try to get the search results
    try:
        log.info(f"Getting search results for query: {query}")

        search_results = serpapi_client.search(
            q=query,
            engine="google",
            gl=serp_config["country"],
        )
    except HTTPConnectionError as e:
        log.error(f"Could not connect to the SerpApi server: {e}")

        error = "Could not connect to the SerpApi server at this time"

        return [], error
    except SerpApiError as e:
        log.error(f"Client error: {e}")

        error = "Client error, check that your Serp API key is correct"

        return [], error
    except Exception as e:
        log.error(f"An unexpected error ocurred: {e}")

        error = "An unexpected error ocurred, please fill an issue in https://github.com/dontic/SEOContentAI"

        return [], error

    log.info("Search results obtained successfully, filtering organic results...")

    organic_results = search_results.get("organic_results", [])

    log.debug(f"Organic results: {organic_results}")

    log.info(
        f"Organic results filtered, getting the top {serp_config['max_results']} URLs..."
    )

    urls = [result["link"] for result in organic_results[: serp_config["max_results"]]]

    log.debug(f"Top URLs: {urls}")

    log.info(f"Returning top {len(urls)} URLs")

    return urls, None

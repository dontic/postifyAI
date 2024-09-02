import streamlit as st
from utils.config_loader import save_config, load_config, create_config


# Main app
def main():
    st.set_page_config(page_title="SEO Article Generator", layout="wide")

    # Initialize session state for form visibility
    if "show_openai_params" not in st.session_state:
        st.session_state.show_openai_params = False
    if "show_claude_params" not in st.session_state:
        st.session_state.show_claude_params = False
    if "show_serp_params" not in st.session_state:
        st.session_state.show_serp_params = False

    # Get or create the config
    param_config = load_config("param_config")
    # Fallback if the config is empty
    if not param_config:
        create_config("param_config")
        param_config = load_config("param_config")

    # Sidebar
    with st.sidebar:

        # ---------------------------------------------------------------------------- #
        #                              Article Parameters                              #
        # ---------------------------------------------------------------------------- #
        st.title("Article Parameters")

        article_params = param_config.get("article_params")

        with st.form("article_params_form"):

            language = st.text_input("Language", value=article_params.get("language"))
            article_type = st.selectbox(
                "Type of article",
                ["Guide", "Informational"],
                index=(0 if article_params.get("article_type") == "Guide" else 1),
            )
            expertise_field = st.text_input(
                "Expertise field",
                value=article_params.get("expertise_field"),
            )
            keyphrase = st.text_input(
                "Keyphrase", value=article_params.get("keyphrase")
            )
            product_name = st.text_input(
                "Product name", value=article_params.get("product_name")
            )
            product_description = st.text_area(
                "Product description",
                value=article_params.get("product_description"),
            )
            product_url = st.text_input(
                "Product URL", value=article_params.get("product_url")
            )

            if st.form_submit_button("Save Article Parameters"):
                article_params = {
                    "language": language,
                    "article_type": article_type,
                    "expertise_field": expertise_field,
                    "keyphrase": keyphrase,
                    "product_name": product_name,
                    "product_description": product_description,
                    "product_url": product_url,
                }
                param_config["article_params"] = article_params
                save_config("param_config", param_config)
                st.success("Article parameters saved!")

        # ---------------------------------------------------------------------------- #
        #                               System Parameters                              #
        # ---------------------------------------------------------------------------- #
        st.title("System Parameters")

        # ----------------------------- AI Model Selector ---------------------------- #
        ai_provider = st.selectbox(
            "Select AI Provider",
            ["OpenAI", "Claude"],
            index=(0 if param_config.get("ai_provider") == "OpenAI" else 1),
        )
        param_config["ai_provider"] = ai_provider
        save_config("param_config", param_config)

        # ----------------------------- OpenAI Parameters ---------------------------- #
        if ai_provider == "OpenAI":

            # Toggle OpenAI Parameters button
            if st.button("OpenAI Parameters"):
                st.session_state.show_openai_params = (
                    not st.session_state.show_openai_params
                )

            if st.session_state.show_openai_params:
                openai_params = param_config.get("openai_params")

                with st.form("openai_params_form"):
                    openai_api_key = st.text_input(
                        "OPENAI_API_KEY",
                        value=openai_params.get("OPENAI_API_KEY"),
                        type="password",
                    )
                    openai_max_tokens = st.number_input(
                        "OPENAI_MAX_TOKENS",
                        value=openai_params.get("OPENAI_MAX_TOKENS"),
                    )
                    openai_temperature = st.slider(
                        "OPENAI_TEMPERATURE",
                        0.0,
                        1.0,
                        openai_params.get("OPENAI_TEMPERATURE"),
                    )
                    openai_max_retries = st.number_input(
                        "OPENAI_MAX_RETRIES",
                        value=openai_params.get("OPENAI_MAX_RETRIES"),
                    )
                    openai_default_model = st.text_input(
                        "OPENAI_DEFAULT_MODEL",
                        value=openai_params.get("OPENAI_DEFAULT_MODEL"),
                    )

                    if st.form_submit_button("Save OpenAI Parameters"):
                        openai_params = {
                            "OPENAI_API_KEY": openai_api_key,
                            "OPENAI_MAX_TOKENS": openai_max_tokens,
                            "OPENAI_TEMPERATURE": openai_temperature,
                            "OPENAI_MAX_RETRIES": openai_max_retries,
                            "OPENAI_DEFAULT_MODEL": openai_default_model,
                        }
                        param_config["openai_params"] = openai_params
                        save_config("param_config", param_config)
                        st.success("OpenAI parameters saved!")

        # --------------------------- Claude AI Parameters --------------------------- #
        else:
            # Toggle Claude AI Parameters button
            if st.button("Claude AI Parameters"):
                st.session_state.show_claude_params = (
                    not st.session_state.show_claude_params
                )

            if st.session_state.show_claude_params:
                claude_params = param_config.get("claude_params")

                with st.form("claude_params_form"):
                    claude_api_key = st.text_input(
                        "CLAUDE_API_KEY",
                        value=claude_params.get("CLAUDE_API_KEY"),
                        type="password",
                    )
                    claude_max_tokens = st.number_input(
                        "CLAUDE_MAX_TOKENS",
                        value=claude_params.get("CLAUDE_MAX_TOKENS"),
                    )
                    claude_temperature = st.slider(
                        "CLAUDE_TEMPERATURE",
                        0.0,
                        1.0,
                        claude_params.get("CLAUDE_TEMPERATURE"),
                    )
                    claude_max_retries = st.number_input(
                        "CLAUDE_MAX_RETRIES",
                        value=claude_params.get("CLAUDE_MAX_RETRIES"),
                    )
                    claude_default_model = st.text_input(
                        "CLAUDE_DEFAULT_MODEL",
                        value=claude_params.get("CLAUDE_DEFAULT_MODEL"),
                    )

                    if st.form_submit_button("Save Claude AI Parameters"):
                        claude_params = {
                            "CLAUDE_API_KEY": claude_api_key,
                            "CLAUDE_MAX_TOKENS": claude_max_tokens,
                            "CLAUDE_TEMPERATURE": claude_temperature,
                            "CLAUDE_MAX_RETRIES": claude_max_retries,
                            "CLAUDE_DEFAULT_MODEL": claude_default_model,
                        }
                        param_config["claude_params"] = claude_params
                        save_config("param_config", param_config)
                        st.success("Claude AI parameters saved!")

        # ---------------------------- SerpAPI Parameters ---------------------------- #
        # Toggle SerpAPI Parameters button
        if st.button("SerpAPI Parameters"):
            st.session_state.show_serp_params = not st.session_state.show_serp_params

        if st.session_state.show_serp_params:
            serp_params = param_config.get("serp_params")

            with st.form("serp_params_form"):
                serp_api_key = st.text_input(
                    "API Key",
                    value=serp_params.get("API_KEY"),
                    type="password",
                )
                serp_location = st.text_input(
                    "Location",
                    value=serp_params.get("LOCATION"),
                )
                serp_language = st.text_input(
                    "Language", value=serp_params.get("LANGUAGE")
                )
                serp_country = st.text_input(
                    "Country", value=serp_params.get("COUNTRY")
                )
                serp_max_results = st.number_input(
                    "MAX_RESULTS", value=serp_params.get("MAX_RESULTS")
                )

                if st.form_submit_button("Save SerpAPI Parameters"):
                    serp_params = {
                        "API_KEY": serp_api_key,
                        "LOCATION": serp_location,
                        "LANGUAGE": serp_language,
                        "COUNTRY": serp_country,
                        "MAX_RESULTS": serp_max_results,
                    }
                    param_config["serp_params"] = serp_params
                    save_config("param_config", param_config)
                    st.success("SerpAPI parameters saved!")

    # ---------------------------------------------------------------------------- #
    #                               Main content area                              #
    # ---------------------------------------------------------------------------- #
    st.title("Generated Article")

    # Initialize session state for the generated text
    if "generated_text" not in st.session_state:
        st.session_state.generated_text = ""

    # Generate button
    if st.button("GENERATE", key="generate_button"):
        # Here you would call your article generation function
        # For now, we'll just update the output text area with a placeholder
        st.session_state.generated_text = "Here is your generated article...\n\nLorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."

    # Text area for output
    st.text_area(
        "Your generated article will appear here...",
        value=st.session_state.generated_text,
        height=400,
        key="output_area",
    )


if __name__ == "__main__":
    main()

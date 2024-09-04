import streamlit as st
from utils.config_loader import save_config, load_config
from article_generator.article_generator import ArticleGenerator


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
                "Type of article (More options coming soon)",
                ["guide"],
                index=0,
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
            ["openai", "claude"],
            index=(0 if param_config.get("ai_provider") == "openai" else 1),
        )
        param_config["ai_provider"] = ai_provider
        save_config("param_config", param_config)

        # ----------------------------- OpenAI Parameters ---------------------------- #
        if ai_provider == "openai":

            # Toggle OpenAI Parameters button
            if st.button("OpenAI Parameters"):
                st.session_state.show_openai_params = (
                    not st.session_state.show_openai_params
                )

            if st.session_state.show_openai_params:
                openai_params = param_config.get("openai_params")

                with st.form("openai_params_form"):
                    openai_api_key = st.text_input(
                        "API Key",
                        value=openai_params.get("api_key"),
                        type="password",
                    )
                    openai_max_tokens = st.number_input(
                        "Max Tokens",
                        value=openai_params.get("max_tokens"),
                    )
                    openai_temperature = st.slider(
                        "Temperature",
                        0.0,
                        1.0,
                        openai_params.get("temperature"),
                    )
                    openai_max_retries = st.number_input(
                        "Max Retries",
                        value=openai_params.get("max_retries"),
                    )
                    openai_default_model = st.text_input(
                        "Default Model",
                        value=openai_params.get("default_model"),
                    )

                    if st.form_submit_button("Save OpenAI Parameters"):
                        openai_params = {
                            "api_key": openai_api_key,
                            "max_tokens": openai_max_tokens,
                            "temperature": openai_temperature,
                            "max_retries": openai_max_retries,
                            "default_model": openai_default_model,
                        }
                        param_config["openai_params"] = openai_params
                        save_config("param_config", param_config)
                        st.success("OpenAI parameters saved!")

        # --------------------------- Claude AI Parameters --------------------------- #
        elif ai_provider == "claude":
            # Toggle Claude AI Parameters button
            if st.button("Claude AI Parameters"):
                st.session_state.show_claude_params = (
                    not st.session_state.show_claude_params
                )

            if st.session_state.show_claude_params:
                claude_params = param_config.get("claude_params")

                with st.form("claude_params_form"):
                    claude_api_key = st.text_input(
                        "API Key",
                        value=claude_params.get("api_key"),
                        type="password",
                    )
                    claude_max_tokens = st.number_input(
                        "Max Tokens",
                        value=claude_params.get("max_tokens"),
                    )
                    claude_temperature = st.slider(
                        "Temperature",
                        0.0,
                        1.0,
                        claude_params.get("temperature"),
                    )
                    claude_max_retries = st.number_input(
                        "Max Retries",
                        value=claude_params.get("max_retries"),
                    )
                    claude_default_model = st.text_input(
                        "Default Model",
                        value=claude_params.get("default_model"),
                    )

                    if st.form_submit_button("Save Claude AI Parameters"):
                        claude_params = {
                            "api_key": claude_api_key,
                            "max_tokens": claude_max_tokens,
                            "temperature": claude_temperature,
                            "max_retries": claude_max_retries,
                            "default_model": claude_default_model,
                        }
                        param_config["claude_params"] = claude_params
                        save_config("param_config", param_config)
                        st.success("Claude AI parameters saved!")

        else:
            st.error("Please select a valid AI provider")

        # ---------------------------- SerpAPI Parameters ---------------------------- #
        # Toggle SerpAPI Parameters button
        if st.button("SerpAPI Parameters"):
            st.session_state.show_serp_params = not st.session_state.show_serp_params

        if st.session_state.show_serp_params:
            serp_params = param_config.get("serp_params")

            with st.form("serp_params_form"):
                serp_api_key = st.text_input(
                    "API Key",
                    value=serp_params.get("api_key"),
                    type="password",
                )
                serp_location = st.text_input(
                    "Location",
                    value=serp_params.get("location"),
                )
                serp_language = st.text_input(
                    "Language", value=serp_params.get("language")
                )
                serp_country = st.text_input(
                    "Country", value=serp_params.get("country")
                )
                serp_max_results = st.number_input(
                    "Max Results", value=serp_params.get("max_results")
                )

                if st.form_submit_button("Save SerpAPI Parameters"):
                    serp_params = {
                        "api_key": serp_api_key,
                        "location": serp_location,
                        "language": serp_language,
                        "country": serp_country,
                        "max_results": serp_max_results,
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
        st.session_state.generated_text = ArticleGenerator().generate()

    # Text area for output
    st.text_area(
        "Your generated article will appear here...",
        value=st.session_state.generated_text,
        height=400,
        key="output_area",
    )


if __name__ == "__main__":
    main()

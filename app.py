import streamlit as st
from utils.config_loader import save_config, load_config
from article_generator.article_generator import ArticleGenerator

from time import sleep
from stqdm import stqdm


# Main app
def main():
    st.set_page_config(page_title="SEO Article Generator", layout="wide")

    # -------------------- Initialize session state variables -------------------- #
    if "show_openai_params" not in st.session_state:
        st.session_state.show_openai_params = False
    if "show_claude_params" not in st.session_state:
        st.session_state.show_claude_params = False
    if "show_serp_params" not in st.session_state:
        st.session_state.show_serp_params = False
    if "generated_text" not in st.session_state:
        st.session_state.generated_text = ""
    if "generating" not in st.session_state:
        st.session_state.generating = False
    if "generation_complete" not in st.session_state:
        st.session_state.generation_complete = False
    if "generation_error" not in st.session_state:
        st.session_state.generation_error = None

    # Get or create the param config when the app starts or re-runs
    param_config = load_config("param_config")

    # Sidebar
    with st.sidebar:

        # ---------------------------------------------------------------------------- #
        #                              Article Parameters                              #
        # ---------------------------------------------------------------------------- #
        st.title("Article Parameters")

        article_params = param_config.get("article_params")

        with st.form("article_params_form"):

            language = st.text_input(
                "Language",
                value=article_params.get("language"),
                disabled=st.session_state.generating,
            )
            article_type = st.selectbox(
                "Type of article (More options coming soon)",
                ["guide"],
                index=0,
                disabled=st.session_state.generating,
            )
            expertise_field = st.text_input(
                "Expertise field",
                value=article_params.get("expertise_field"),
                disabled=st.session_state.generating,
            )
            keyphrase = st.text_input(
                "Keyphrase",
                value=article_params.get("keyphrase"),
                disabled=st.session_state.generating,
            )
            product_name = st.text_input(
                "Product name",
                value=article_params.get("product_name"),
                disabled=st.session_state.generating,
            )
            product_description = st.text_area(
                "Product description",
                value=article_params.get("product_description"),
                disabled=st.session_state.generating,
            )
            product_url = st.text_input(
                "Product URL",
                value=article_params.get("product_url"),
                disabled=st.session_state.generating,
            )

            if st.form_submit_button(
                "Save Article Parameters",
                disabled=st.session_state.generating,
            ):
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
            disabled=st.session_state.generating,
        )
        param_config["ai_provider"] = ai_provider
        save_config("param_config", param_config)

        # ----------------------------- OpenAI Parameters ---------------------------- #
        if ai_provider == "openai":

            # Toggle OpenAI Parameters button
            if st.button(
                "OpenAI Parameters",
                disabled=st.session_state.generating,
            ):
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
                        disabled=st.session_state.generating,
                    )
                    openai_max_tokens = st.number_input(
                        "Max Tokens",
                        value=openai_params.get("max_tokens"),
                        disabled=st.session_state.generating,
                    )
                    openai_temperature = st.slider(
                        "Temperature",
                        0.0,
                        1.0,
                        openai_params.get("temperature"),
                        disabled=st.session_state.generating,
                    )
                    openai_max_retries = st.number_input(
                        "Max Retries",
                        value=openai_params.get("max_retries"),
                        disabled=st.session_state.generating,
                    )
                    openai_default_model = st.text_input(
                        "Default Model",
                        value=openai_params.get("default_model"),
                        disabled=st.session_state.generating,
                    )

                    if st.form_submit_button(
                        "Save OpenAI Parameters",
                        disabled=st.session_state.generating,
                    ):
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
            if st.button(
                "Claude AI Parameters",
                disabled=st.session_state.generating,
            ):
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
                        disabled=st.session_state.generating,
                    )
                    claude_max_tokens = st.number_input(
                        "Max Tokens",
                        value=claude_params.get("max_tokens"),
                        disabled=st.session_state.generating,
                    )
                    claude_temperature = st.slider(
                        "Temperature",
                        0.0,
                        1.0,
                        claude_params.get("temperature"),
                        disabled=st.session_state.generating,
                    )
                    claude_max_retries = st.number_input(
                        "Max Retries",
                        value=claude_params.get("max_retries"),
                        disabled=st.session_state.generating,
                    )
                    claude_default_model = st.text_input(
                        "Default Model",
                        value=claude_params.get("default_model"),
                        disabled=st.session_state.generating,
                    )

                    if st.form_submit_button(
                        "Save Claude AI Parameters",
                        disabled=st.session_state.generating,
                    ):
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
        if st.button(
            "SerpAPI Parameters",
            disabled=st.session_state.generating,
        ):
            st.session_state.show_serp_params = not st.session_state.show_serp_params

        if st.session_state.show_serp_params:
            serp_params = param_config.get("serp_params")

            with st.form("serp_params_form"):
                serp_api_key = st.text_input(
                    "API Key",
                    value=serp_params.get("api_key"),
                    type="password",
                    disabled=st.session_state.generating,
                )
                serp_location = st.text_input(
                    "Location",
                    value=serp_params.get("location"),
                    disabled=st.session_state.generating,
                )
                serp_language = st.text_input(
                    "Language",
                    value=serp_params.get("language"),
                    disabled=st.session_state.generating,
                )
                serp_country = st.text_input(
                    "Country",
                    value=serp_params.get("country"),
                    disabled=st.session_state.generating,
                )
                serp_max_results = st.number_input(
                    "Max Results",
                    value=serp_params.get("max_results"),
                    disabled=st.session_state.generating,
                )

                if st.form_submit_button(
                    "Save SerpAPI Parameters",
                    disabled=st.session_state.generating,
                ):
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

    def start_generation():
        if not st.session_state.generating:
            st.session_state.generating = True
            st.session_state.generation_complete = False
            st.rerun()

    # If the generation process is in progress
    if st.session_state.generating and not st.session_state.generation_complete:

        progress_text = "Operation in progress. Please wait."
        progress_bar = st.progress(0, text=progress_text)

        with st.status("Generating article...", expanded=True) as status:

            text, error = ArticleGenerator().generate(progress_bar)

            status.update(label="Article generated!", state="complete", expanded=True)

            st.session_state.generated_text = text
            st.session_state.generation_error = error

            st.session_state.generating = False
            st.session_state.generation_complete = True

            st.rerun()

    # If the generation process is not in progress and there wasn't a previous generation
    # Display the GENERATE button only
    elif not st.session_state.generating and not st.session_state.generation_complete:
        if st.button(
            "GENERATE" if not st.session_state.generation_complete else "REGENERATE",
            key="generate_button",
            use_container_width=True,
            type="primary",
        ):
            start_generation()

    # If the generation process is not in progress and there was a previous generation
    else:

        if st.session_state.generation_error:
            st.error(
                f"Error generating article!\n\n{st.session_state.generation_error}"
            )
        else:
            st.success("Article generated successfully!")

        # Buttons for actions
        col1, buff, col3 = st.columns(3)

        with col1:
            if st.button(
                "REGENERATE",
                key="regenerate_button",
                type="primary",
            ):
                start_generation()

        with col3:
            if st.download_button(
                "Download Markdown",
                st.session_state.generated_text,
                file_name="generated_article.md",
            ):
                st.write("Article downloaded!")

        # Display generated text
        st.markdown(
            st.session_state.generated_text or "Your article will appear here..."
        )


if __name__ == "__main__":
    main()

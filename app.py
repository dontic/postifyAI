import streamlit as st
from article_generator.article_generator import ArticleGenerator
from utils.config_manager import ConfigManager


# Main app
def main():

    # Initialize the config manager
    config_manager = ConfigManager()

    # Load the parameters from the config file
    params = config_manager.load_params()

    # Set the page config
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

    # --------------------------------- Functions -------------------------------- #
    def get_ai_provider_index(ai_provider: str, ai_provider_list: list[str]) -> int:
        """
        Get the index of the AI provider in the list

        Args:
            ai_provider (str): The AI provider to get the index of
            ai_provider_list (list[str]): The list of AI providers

        Returns:
            int: The index of the AI provider in the list
        """
        return ai_provider_list.index(ai_provider)

    # --------------------------------- Callbacks -------------------------------- #
    def save_article_params():
        params["article_params"] = {
            "language": st.session_state.language,
            "article_type": st.session_state.article_type,
            "expertise_field": st.session_state.expertise_field,
            "keyphrase": st.session_state.keyphrase,
            "product_name": st.session_state.product_name,
            "product_description": st.session_state.product_description,
            "product_url": st.session_state.product_url,
        }
        config_manager.save_params(params)

        st.toast("Article parameters saved!", icon="✅")

    def save_ai_provider():
        print(st.session_state.ai_provider)
        params["ai_provider"] = st.session_state.ai_provider
        config_manager.save_params(params)

    def save_openai_params():
        openai_params = {
            "api_key": st.session_state.openai_api_key,
            "max_tokens": st.session_state.openai_max_tokens,
            "temperature": st.session_state.openai_temperature,
            "max_retries": st.session_state.openai_max_retries,
            "default_model": st.session_state.openai_default_model,
        }
        params["openai_params"] = openai_params
        config_manager.save_params(params)
        st.success("OpenAI parameters saved!")

    # --------------------------------- Layout ---------------------------------- #

    # Sidebar
    with st.sidebar:

        # ---------------------------------------------------------------------------- #
        #                              Article Parameters                              #
        # ---------------------------------------------------------------------------- #
        st.title("Article Parameters")

        article_params = params.get("article_params")

        # Article parameters form
        with st.form("article_params_form"):
            st.text_input(
                "Language",
                key="language",
                value=article_params.get("language"),
                disabled=st.session_state.generating,
            )
            st.selectbox(
                "Type of article (More options coming soon)",
                ["guide"],
                key="article_type",
                index=0,
                disabled=st.session_state.generating,
            )
            st.text_input(
                "Expertise field",
                key="expertise_field",
                value=article_params.get("expertise_field"),
                disabled=st.session_state.generating,
            )
            st.text_input(
                "Keyphrase",
                key="keyphrase",
                value=article_params.get("keyphrase"),
                disabled=st.session_state.generating,
            )
            st.text_input(
                "Product name",
                key="product_name",
                value=article_params.get("product_name"),
                disabled=st.session_state.generating,
            )
            st.text_area(
                "Product description",
                key="product_description",
                value=article_params.get("product_description"),
                disabled=st.session_state.generating,
            )
            st.text_input(
                "Product URL",
                key="product_url",
                value=article_params.get("product_url"),
                disabled=st.session_state.generating,
            )
            st.form_submit_button(
                "Save Article Parameters",
                disabled=st.session_state.generating,
                on_click=save_article_params,
            )

        # ---------------------------------------------------------------------------- #
        #                               System Parameters                              #
        # ---------------------------------------------------------------------------- #
        st.title("System Parameters")

        # --------------------------- AI provider Selector --------------------------- #
        ai_provider_list = ["openai", "claude"]
        ai_provider = params.get("ai_provider")

        st.selectbox(
            "Select AI Provider",
            ai_provider_list,
            key="ai_provider",
            index=(get_ai_provider_index(ai_provider, ai_provider_list)),
            disabled=st.session_state.generating,
            on_change=save_ai_provider,
        )

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
                openai_params = params.get("openai_params")

                with st.form("openai_params_form"):
                    st.text_input(
                        "API Key",
                        key="openai_api_key",
                        value=openai_params.get("api_key"),
                        type="password",
                        disabled=st.session_state.generating,
                    )
                    st.number_input(
                        "Max Tokens",
                        key="openai_max_tokens",
                        value=openai_params.get("max_tokens"),
                        disabled=st.session_state.generating,
                    )
                    st.slider(
                        "Temperature",
                        0.0,
                        1.0,
                        openai_params.get("temperature"),
                        key="openai_temperature",
                        disabled=st.session_state.generating,
                    )
                    st.number_input(
                        "Max Retries",
                        key="openai_max_retries",
                        value=openai_params.get("max_retries"),
                        disabled=st.session_state.generating,
                    )
                    st.text_input(
                        "Default Model",
                        key="openai_default_model",
                        value=openai_params.get("default_model"),
                        disabled=st.session_state.generating,
                    )
                    st.form_submit_button(
                        "Save OpenAI Parameters",
                        disabled=st.session_state.generating,
                        on_click=save_openai_params,
                    )

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
                claude_params = params.get("claude_params")

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
                        params["claude_params"] = claude_params
                        config_manager.save_params(params)
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
            serp_params = params.get("serp_params")

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
                    params["serp_params"] = serp_params
                    config_manager.save_params(params)
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

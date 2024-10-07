import json
from pathlib import Path
from logging_setup import setup_logger

log = setup_logger(__name__)


class ConfigManager:
    def __init__(self):
        log.info("Initializing Config Manager...")

        # Define the base directory
        self.base_dir = Path(__file__).resolve().parent.parent

        # Ensure the data, params directories exist
        (self.base_dir / "data" / "params").mkdir(parents=True, exist_ok=True)
        self.params_dir = self.base_dir / "data" / "params"

        # Define the params path
        self.params_path = self.params_dir / "params.json"

        # Ensure the params file xist
        if not self.params_path.exists():
            log.info("No params file found, creating default params file...")

            with open(self.base_dir / "default_params.json", "r") as f:
                default_params = json.load(f)
                self.save_params(default_params)

    def load_params(self):
        """
        Load the params from the data directory

        Returns:
            dict: The params
        """

        log.info("Loading params...")

        # Load the data
        with open(self.params_path, "r") as f:
            return json.load(f)

    def save_params(self, params):
        """
        Save the params to the data directory

        Args:
            params (dict): The params to save

        Returns:
            None
        """

        log.info("Saving params...")

        # Save the params
        with open(self.params_path, "w") as f:
            json.dump(params, f, indent=4, sort_keys=True)

    def load_prompts() -> dict:
        """
        Load the prompt config file

        Returns:
            dict: The loaded prompts file
        """

        log.info("Loading prompts...")

        # Define the base directory
        base_dir = Path(__file__).resolve().parent.parent

        # Define the prompts path
        prompts_path = base_dir / "article_generator" / "prompts.json"

        # Load the config
        with open(prompts_path, "r") as f:
            return json.load(f)

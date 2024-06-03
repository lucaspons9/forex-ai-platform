import yaml

from utils.logger import configure_logger

LOGGER = configure_logger(__file__)


def read_config(file_path):
    """
    Read and parse a YAML configuration file.

    Parameters:
        file_path (str): The path to the YAML configuration file.

    Returns:
        dict: The parsed configuration as a dictionary.

    Raises:
        FileNotFoundError: If the file does not exist.
        yaml.YAMLError: If the file contains invalid YAML.
        Exception: For any other exceptions.
    """
    try:
        with open(file_path, "r") as file:
            config = yaml.safe_load(file)
        return config
    except FileNotFoundError:
        LOGGER.error(f"The configuration file at {file_path} does not exist.")
        raise FileNotFoundError(
            f"The configuration file at {file_path} does not exist."
        )
    except yaml.YAMLError as e:
        LOGGER.error(f"Error parsing YAML file at {file_path}: {e}")
        raise ValueError(f"Error parsing YAML file at {file_path}: {e}")
    except Exception as e:
        LOGGER.error(
            f"An unexpected error occurred while reading the configuration file at {file_path}: {e}"
        )
        raise Exception(
            f"An unexpected error occurred while reading the configuration file at {file_path}: {e}"
        )

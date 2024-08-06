import os
from datetime import date
from typing import Tuple

import streamlit as st
import yaml  # type: ignore
from cloud_storage_wrapper.oci_access.config import OCI_Config_Base
from cloud_storage_wrapper.oci_access.files import FilesOCI
from cloud_storage_wrapper.oci_access.pandas import create_PandasOCI_from_dict
from cloud_storage_wrapper.oci_access.pandas import PandasOCI
from tpa_analytics_engine.api import Forecast


@st.cache_resource  # This caches accross all sessions
def load_config_dict(todays_date: date, config_path: str) -> dict:
    """Loads the config file for the app and returns the config as a dict.

    Args:
        todays_date (date): A date, this argument is not used but enables streamlit caching which is refreshed daily.
        config_path (str): The path to the config file. This can be a local file path or a URL to a .yaml file on Github.

    Returns:
        dict: A dictionary containing the contents of the content file config.yaml.
    """
    if config_path.startswith("http"):
        import urllib.request

        config = yaml.safe_load(urllib.request.urlopen(config_path))
    else:
        with open(config_path, "r") as file:
            config = yaml.safe_load(file)

    # Add todays_date to the config
    config["todays_date"] = todays_date

    return config


@st.cache_resource  # This caches accross all sessions
def create_pandasOCI(config_dict: dict) -> PandasOCI:
    """
    This function provides a PandasOCI object based on the provided config_dict.

    Args:
        config_dict (dict): A dictionary containing the app configuration.

    Returns:
        PandasOCI: An instance of PandasOCI created from the config_dict.
    """
    return create_PandasOCI_from_dict(configDict=config_dict)


@st.cache_resource  # This caches accross all sessions
def create_filesOCI(config_dict: dict) -> FilesOCI:
    """
    This function provides a FilesOCI object based on the provided config_dict.

    Args:
        config_dict (dict): A dictionary containing the app configuration.

    Returns:
        FilesOCI: An instance of FilesOCI created from the config_dict.
    """
    configDict_Base = OCI_Config_Base(**config_dict["oci_config"]).model_dump()
    return FilesOCI(**configDict_Base)


@st.cache_resource  # This caches accross all sessions
def create_Forecast(todays_date: date) -> Forecast:
    """
    This function provides a `Forecast` object based on the config path.

    Args:
        todays_date (date): A date, this argument is not used but enables streamlit caching which is refreshed daily.

    Returns:
        Forecast: An instance of `Forecast` created using the configuration file located at "configs/config.yaml".
    """

    return Forecast(config_path=os.getenv("CONFIG_PATH", "configs/config.yaml"))


@st.cache_resource  # This caches accross all sessions
def load_language_config_dict(config_dict: dict) -> dict:
    """This function loads the language_config and returns it as a dict.

    Args:
        config_dict (dict): A dictionary with the app configuration.

    Returns:
        dict: The language_config as a dict.
    """
    # Load the language config
    with open(config_dict.get("language_config", ""), "r") as file:
        # Load the YAML data
        language_dict: dict = yaml.safe_load(file)

    # Add leading spaces to the weekday_list for formatting in the relevant graph
    for forecast_dict in language_dict.get("forecast", {}).values():
        weekday_list = forecast_dict.get("weekday_list")
        for i in range(len(weekday_list)):
            weekday_list[i] = " " * (len(weekday_list) - i) + weekday_list[i]

    return language_dict


def create_config_from_env() -> Tuple[dict, dict]:
    """A function that loads the app and language config based on the environment variable "CONFIG_PATH" and returns them as a tuple.

    Returns:
        Tuple[dict, dict]: A tuple containing the app config and the language dict.
    """
    config_dict = load_config_dict(
        todays_date=date.today(),
        config_path=os.getenv("CONFIG_PATH", "configs/config.yaml"),
    )
    language_dict = load_language_config_dict(config_dict=config_dict)

    return (config_dict, language_dict)

import time
from typing import Dict

import numpy as np
import pandas as pd
import streamlit as st
from cloud_storage_wrapper.oci_access.pandas import PandasOCI
from tpa_analytics_engine.api import Forecast


@st.cache_resource  # This caches accross all sessions
def loadBaseDFs(config_dict: dict, _pandas_connection: PandasOCI) -> dict:
    """
    A function to load base DataFrames (data frames which are used by different components of the app) based on the provided config dictionary and PandasOCI connection object.

    Parameters:
        config_dict (dict): A dictionary containing the app configuration. Streamlit caches this function based on the config dict. Since the date is in the config dict, this function is also cached on the date.
        _pandas_connection (PandasOCI): An instance of the PandasOCI connection. Streamlit doesn't evaluate this argument for caching.

    Returns:
        dict: A dictionary containing the loaded DataFrames.
    """
    # Initialize loaded_dfs dictionary
    loaded_dfs = {}
    # Get the df_config_dict, specifying which dfs to load
    df_config_dict = config_dict.get("df_config", {})
    # Load the dfs if there is a pre_load key in the sub dict for that df
    for df_dict_key in df_config_dict.keys():
        if "pre_load" in df_config_dict.get(df_dict_key):
            # Add the df to the loaded_dfs dict by retrieving  the df via _pandas_connection
            loaded_dfs[df_dict_key] = _pandas_connection.retrieve_df(
                path=df_config_dict.get(df_dict_key).get("df_path"),
                df_format=df_config_dict.get(df_dict_key).get("df_format"),
            )

    return loaded_dfs


@st.cache_resource  # This caches accross all sessions
def makeForecast(
    config_dict: dict, station: str, gas_type: str, _forecaster: Forecast
) -> Dict[str, pd.DataFrame]:
    """
    A function that makes a forecast based on the provided station and sorte utilizing a _forecaster object.
    It returns a dictionary containing the forecast DataFrame, summary DataFrames for weekday, hour, and trend.

    Parameters:
        config_dict (dict): A dictionary containing the app configuration. Streamlit caches this function based on the config dict. Since the date is in the config dict, this function is also cached on the date.
        station (str): The station for which the forecast is made.
        gas_type (str): The gas_type for which to make the price forecast.
        _forecaster (Forecast): An instance of the Forecast class used for forecasting. Streamlit doesn't evaluate this argument for caching.

    Returns:
        Dict[str, pd.DataFrame]: A dictionary mapping names to the different DataFrames resulting from the forecast.
    """
    start = time.time()
    # Use the _forecaster to load the relevant df for station and gas_type
    _forecaster.load_df(station=station, sorte=gas_type)
    print("Loading the df took: ", time.time() - start)
    start = time.time()
    # Create the forecast
    forecast_df = _forecaster.create_forecast()
    # Filter the df on the last and previous date
    max_date_pre = forecast_df.query("is_last==0")["Day"].max()
    forecast_df = forecast_df[
        (forecast_df["is_last"] == 1) | (forecast_df["Day"] == max_date_pre)
    ].copy()
    # Fill the pred price with the actual price (for the previous date)
    forecast_df["pred"] = forecast_df["pred"].fillna(forecast_df["price"])
    # Filter relevant columns
    forecast_df = forecast_df[["Day_Hours", "pred", "is_last", "hour_format"]]
    # Add a space in front of the time_string to keep sortation by previous date and last date
    forecast_df["hour_format"] = np.where(
        forecast_df.is_last == 1,
        forecast_df["hour_format"],
        " " + forecast_df["hour_format"],
    )

    print("Finishing forecasting: ", time.time() - start)
    # Return DataFrames as a dict
    return {
        "forecast_df": forecast_df,
        "summary_weekday_df": _forecaster.create_summaries(
            groupCol="day_of_week", centralize_mean=True
        )
        .reset_index()
        .rename(columns={"price": "diff"}),
        "summary_hour_df": _forecaster.create_summaries(
            groupCol="hour_format", centralize_mean=True
        )
        .reset_index()
        .rename(columns={"price": "diff"}),
        "summary_trend_df": _forecaster.create_summaries(
            groupCol="week", centralize_mean=False
        ).reset_index(),
    }

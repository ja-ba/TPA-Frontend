from datetime import date

import pandas as pd
import streamlit as st
from tpa_frontend.config_handler.load_configs import create_config_from_env
from tpa_frontend.config_handler.load_configs import create_Forecast
from tpa_frontend.config_handler.load_configs import create_pandasOCI
from tpa_frontend.data_loader.load import loadBaseDFs
from tpa_frontend.streamlit_elements.mainframe import fill_main_frame
from tpa_frontend.streamlit_elements.sidebar import createLanguageSelection
from tpa_frontend.streamlit_elements.sidebar import createSidebar
from tpa_frontend.streamlit_elements.sidebar import sidebar_lower_content


def run_app() -> None:
    """Runs the streamlit app when called."""
    ##############################################################################
    ####### Configure the app ####################################################
    ##############################################################################
    today = date.today()
    # Loads the config file
    config_dict, language_dict = create_config_from_env()
    pandasOCI = create_pandasOCI(config_dict=config_dict)
    base_df_dict = loadBaseDFs(config_dict=config_dict, _pandas_connection=pandasOCI)
    forecaster = create_Forecast(todays_date=today)

    ##############################################################################
    ####### Configure the app sidebar ############################################
    ##############################################################################
    with st.sidebar:
        selected_language = createLanguageSelection(language_dict=language_dict)
        selectedSideBar = createSidebar(
            language_dict=language_dict, language_selection=selected_language
        )

        selected_station, selected_gas_type = "", ""
        if selectedSideBar == "forecast":
            selected_station, selected_gas_type = sidebar_lower_content(
                language_dict=language_dict,
                language_selection=selected_language,
                selectedSideBar=selectedSideBar,
                station_dict=base_df_dict.get("station_info_30", pd.DataFrame())
                .set_index("Tankstellen_Name")["short_id"]
                .to_dict(),
            )  # type: ignore

    fill_main_frame(
        config_dict=config_dict,
        language_dict=language_dict,
        selectedSideBar=selectedSideBar,
        language_selection=selected_language,
        selected_station=selected_station,
        selected_gas_type=selected_gas_type,
        forecaster=forecaster,
    )

if __name__ == "__main__":
    run_app()

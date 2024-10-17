from typing import Optional
from typing import Union

import streamlit as st
from streamlit_option_menu import option_menu
from tpa_frontend.config_handler.load_configs import create_config_from_env

language_dict = create_config_from_env()[1]


def createSidebar(language_dict: dict, language_selection: str) -> str:
    """A to build and evaluate the sidebar.

    Args:
        language_dict (dict): A dictionary containing the language configuration.
        language_selection (str): The selected language in which to display the page.

    Returns:
        str: The selected element from the sidebar
    """
    selection = option_menu(
        menu_title=list(
            language_dict.get("sidebar_upper", {}).get(language_selection).keys()
        )[0],
        options=list(
            language_dict.get("sidebar_upper", {}).get(language_selection).keys()
        )[1:],
        icons=language_dict.get("sidebar_upper", {}).get("symbols"),
    )

    return (
        language_dict.get("sidebar_upper", {})
        .get(language_selection, {})
        .get(selection)
    )


def createLanguageSelection(language_dict: dict) -> str:
    """A function creating the language selection in the upper left side bar.

    Args:
        language_dict (dict): A dictionary containing the language configuration.

    Returns:
        str: The values of the language selection (either 'Ger' or 'Eng').
    """

    # Set markdowns for flags
    st.markdown(
        language_dict.get("markdown", {}).get("english_flag"), unsafe_allow_html=True
    )
    st.markdown(
        language_dict.get("markdown", {}).get("german_flag"), unsafe_allow_html=True
    )

    # Language selection via the previously specified flags
    language_selection = st.radio(
        label="Language",
        options=["Eng", "Ger"],
        format_func=lambda x: " "
        if x == "Eng"
        else "  ",  # display an empty option label, so that text doesn't overlay flag
        horizontal=True,
        key="SELECT_language",
    )
    return language_selection or ""


def sidebar_lower_content(
    language_dict: dict,
    language_selection: str,
    selectedSideBar: str,
    station_dict: dict = {},
) -> Optional[Union[tuple, str]]:
    """A function to dynamically create the  lower part of the sidebar depending on the selected sidebar element.

    Args:
        language_dict (dict): A dictionary containing the language configuration.
        language_selection (str): The selected language in which to display the elements.
        selectedSideBar (str): The selected sidebar element, controlling which page is shown in the mainframe.
        station_dict (dict, optional): A dictionary mapping station names to their corresponding IDs. This is required for the "forecast" lower sidebar. Defaults to {}.

    Returns:
        Optional[tuple]: A tuple of selected station and gas_type
    """
    if selectedSideBar == "forecast":
        selected_station = station_dict.get(
            st.selectbox(
                label=language_dict.get("sidebar_lower", {})
                .get(selectedSideBar)
                .get(language_selection)[0],
                help=language_dict.get("sidebar_lower", {})
                .get(selectedSideBar)
                .get(language_selection)[1],
                options=station_dict.keys(),
                index=None,
                key="SELECT_station",
            )
        )
        selected_gas_type = st.radio(
            label=language_dict.get("sidebar_lower", {})
            .get(selectedSideBar)
            .get(language_selection)[2],
            options=["E5", "E10", "Diesel"],
            horizontal=True,
            key="SELECT_gas_type_forecast",
        )

        return (selected_station, selected_gas_type)

    elif selectedSideBar == "maps":
        selected_gas_type = st.radio(
            label=language_dict.get("sidebar_lower", {})
            .get(selectedSideBar)
            .get(language_selection),
            options=["E5", "E10", "Diesel"],
            horizontal=True,
            key="SELECT_gas_type_map",
        )

        return selected_gas_type

    else:
        return None

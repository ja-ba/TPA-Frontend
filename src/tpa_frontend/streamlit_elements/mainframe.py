import pandas as pd
import streamlit as st
from tpa_frontend.charts.create import create_bar_chart
from tpa_frontend.charts.create import create_forecast_chart
from tpa_frontend.charts.create import create_trend_chart
from tpa_frontend.data_loader.load import makeForecast


def fill_main_frame(
    config_dict: dict,
    language_dict: dict,
    selectedSideBar: str,
    language_selection: str,
    **kwargs,
) -> None:
    """A function filling the mainframe of the app.

    Args:
        config_dict (dict): A dictionary containing the app configuration.
        language_dict (dict): A dictionary containing the language configuration.
        selectedSideBar (str): The selected sidebar element, controlling which page is shown in the mainframe.
        language_selection (str): The selected language in which to display the page.
        **kwargs: Optional keyword arguments.
    """
    kwargs_dict = kwargs

    if selectedSideBar == "welcome":
        st.markdown(body=language_dict.get("welcome_text", {}).get(language_selection))

    if selectedSideBar == "forecast":
        if kwargs_dict.get("selected_station") is None:
            st.text(
                language_dict.get(selectedSideBar, {})
                .get(language_selection)
                .get("please_choose")
            )

        else:
            # Initialize the tabs
            tab1, tab2 = st.tabs(
                [
                    language_dict.get(selectedSideBar, {})
                    .get(language_selection)
                    .get("tab_title1"),
                    language_dict.get(selectedSideBar, {})
                    .get(language_selection)
                    .get("tab_title2"),
                ]
            )

            # Create the forecasts:
            forecast_summary_dict = makeForecast(config_dict=config_dict, station=kwargs_dict.get("selected_station"), gas_type=kwargs_dict.get("selected_gas_type").lower(), _forecaster=kwargs_dict.get("forecaster"))  # type: ignore

            with tab1:
                st.write(
                    f"tab1 selected, short_id: {kwargs_dict.get('selected_station')}, language: {language_selection}"
                )
                st.markdown(
                    language_dict.get(selectedSideBar, {})
                    .get(language_selection)
                    .get("page_title_forecast")
                )
                chart = create_forecast_chart(
                    df=forecast_summary_dict.get("forecast_df", pd.DataFrame()),
                    language_selection=language_selection,
                )
                # chart["usermeta"] = {
                #     "embedOptions": { "format_locale": "de-DE" , "actions": False,}}
                # chart.configure(locale="de-DE")
                st.altair_chart(chart, theme=None)  # type: ignore

            with tab2:
                st.write(
                    f"tab2 selected, short_id: {kwargs_dict.get('selected_station')}"
                )
                st.markdown(
                    language_dict.get(selectedSideBar, {})
                    .get(language_selection)
                    .get("page_title_impact")
                )
                st.write(
                    language_dict.get(selectedSideBar, {})
                    .get(language_selection)
                    .get("chart_title_hour")
                )
                st.altair_chart(create_bar_chart(df=forecast_summary_dict.get("summary_hour_df"), language_selection=language_selection), use_container_width=True, theme=None)  # type: ignore
                st.write(
                    language_dict.get(selectedSideBar, {})
                    .get(language_selection)
                    .get("chart_title_weekday")
                )
                st.altair_chart(create_bar_chart(df=forecast_summary_dict.get("summary_weekday_df"), language_selection=language_selection), use_container_width=True)  # type: ignore
                st.write(
                    language_dict.get(selectedSideBar, {})
                    .get(language_selection)
                    .get("chart_title_trend")
                )
                st.altair_chart(create_trend_chart(df=forecast_summary_dict.get("summary_trend_df"), language_selection=language_selection), use_container_width=True)  # type: ignore

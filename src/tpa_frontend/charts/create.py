# Import packages
from typing import Any

import altair as alt
import numpy as np
import pandas as pd
from tpa_frontend.config_handler.load_configs import create_config_from_env

language_dict = create_config_from_env()[1]


def _provide_interactive_chart_elements(
    language_selection: str,
    x_field: str,
    y_field: str,
    decimals: int,
    df: pd.DataFrame,
    current_chart: Any,
) -> dict:
    """A helper function to create the interactive elements of the chart.

    Args:
        language_selection (str): The language selection from the app.
        x_field (str): The field in the data frame to be plotted on the x-axis.
        y_field (str): The field in the data frame to be plotted on the y-axis.
        decimals (int): The number of decimals to display in the chart markers.
        df (pd.DataFrame): The df with the data to plot.
        current_chart (Any): The chart to which to add the interactive elements.

    Returns:
        dict: A dictionary of the interactive chart elements.
    """
    # Set the correct number formatting based on the langage selection
    alt.renderers.set_embed_options(
        format_locale="de-DE" if language_selection == "Ger" else "en-IE"
    )

    # Create a selection that chooses the nearest point & selects based on x-value
    nearest = alt.selection_point(
        nearest=True, on="mouseover", fields=[x_field], empty=False
    )

    # Transparent selectors across the chart. This is what tells us
    selectors = (
        alt.Chart(df)
        .mark_point()
        .encode(x=f"{x_field}:N", opacity=alt.value(0), tooltip=alt.value(None))
        .add_params(nearest)
    )

    # Draw a rule at the location of the selection
    rules = (
        alt.Chart(df)
        .mark_rule(color="gray")
        .encode(
            x=f"{x_field}:N",
        )
        .transform_filter(nearest)
    )

    # Draw points on the line, and highlight based on selection
    points = current_chart.mark_point().encode(
        opacity=alt.condition(nearest, alt.value(1), alt.value(0))  # type: ignore
    )

    # Draw text labels near the points, and highlight based on selection
    text = current_chart.mark_text(align="left", dx=5, dy=-5).encode(
        text=alt.condition(
            nearest,
            alt.Text(f"{y_field}:Q", format=f".{decimals}f"),
            alt.value(" "),
        )
    )

    return {
        "current_chart": current_chart,
        "selectors": selectors,
        "rules": rules,
        "points": points,
        "text": text,
    }


def create_forecast_chart(df: pd.DataFrame, language_selection: str) -> alt.LayerChart:
    """Creates the forecast chart.

    Args:
        df (pd.DataFrame): The df containing the forecast data.
        language_selection (str): The language selection from the app.

    Returns:
        alt.LayerChart: The altair chart to display in the app.
    """
    legend_name: str = (
        language_dict.get("forecast", {})
        .get(language_selection, {})
        .get("legend_name", "")
    )
    legend_forecast: str = (
        language_dict.get("forecast", {})
        .get(language_selection, {})
        .get("legend_forecast")
    )
    legend_yesterday: str = (
        language_dict.get("forecast", {})
        .get(language_selection, {})
        .get("legend_yesterday")
    )

    df[legend_name] = np.where(df.is_last == 1, legend_forecast, legend_yesterday)
    x_field, y_field = "time_string", "pred"

    scale = alt.Scale(
        domain=[legend_forecast, legend_yesterday],
        range=["#4FA095", "#153462"],
    )

    line = (
        alt.Chart(df)
        .mark_line(interpolate="step")
        .encode(
            x=alt.X(
                f"{x_field}:N",
                title=language_dict.get("forecast", {})
                .get(language_selection)
                .get("x_title"),
            ),
            y=alt.Y(
                f"{y_field}:Q",
                scale=alt.Scale(zero=False),
                title=language_dict.get("forecast", {})
                .get(language_selection)
                .get("y_title"),
            ),
            color=alt.Color(
                f"{legend_name}:N",
                scale=scale,
                legend=alt.Legend(
                    orient="top-right",
                    offset=1,
                    padding=2,
                    direction="vertical",
                    titleAnchor="start",
                ),
            ),
        )
    )

    shared_elements = _provide_interactive_chart_elements(
        language_selection=language_selection,
        x_field=x_field,
        y_field=y_field,
        decimals=2,
        df=df,
        current_chart=line,
    )

    return alt.layer(
        line,
        shared_elements.get("selectors"),
        shared_elements.get("points"),
        shared_elements.get("rules"),
        shared_elements.get("text"),
    ).properties(width=1000, height=400)


def create_bar_chart(df: pd.DataFrame, language_selection: str) -> alt.LayerChart:
    """Creates the bar charts for the price impacts.

    Args:
        df (pd.DataFrame): The df containing the bar chart data, i.e. price impacts.
        language_selection (str): The language selection from the app.

    Returns:
        alt.LayerChart: The altair chart to display in the app.
    """
    x_field, y_field = df.columns[0], df.columns[1]

    y_axis_title: str = (
        language_dict.get("forecast", {})
        .get(language_selection, {})
        .get("y_title_barchart", "")
    )
    if x_field == "hour":
        x_axis_title: str = (
            language_dict.get("forecast", {})
            .get(language_selection, {})
            .get("x_title_hour", "")
        )
        bar_color = "#A3C7D6"
        decimals = 2
    elif x_field == "day_of_week":
        x_axis_title = (
            language_dict.get("forecast", {})
            .get(language_selection, {})
            .get("x_title_hour", "")
        )
        bar_color = "#9F73AB"
        decimals = 3

    bar = (
        alt.Chart(df)
        .mark_bar(color=bar_color)
        .encode(
            x=alt.X(
                f"{x_field}:N",
                title=x_axis_title,
            ),
            y=alt.Y(
                f"{y_field}:Q",
                title=y_axis_title,
            ),
        )
    )

    shared_elements = _provide_interactive_chart_elements(
        language_selection=language_selection,
        x_field=x_field,
        y_field=y_field,
        decimals=decimals,
        df=df,
        current_chart=bar,
    )

    return alt.layer(
        bar,
        shared_elements.get("selectors"),
        shared_elements.get("points"),
        shared_elements.get("text"),
    ).properties(width=800, height=300)


def create_trend_chart(df: pd.DataFrame, language_selection: str) -> alt.LayerChart:
    """Creates the longterm trend chart.

    Args:
        df (pd.DataFrame): The df containing the longterm trend data.
        language_selection (str): The language selection from the app.

    Returns:
        alt.LayerChart: The altair chart to display in the app.
    """

    x_field, y_field = df.columns[0], df.columns[1]

    y_axis_title: str = (
        language_dict.get("forecast", {}).get(language_selection, {}).get("y_title", "")
    )
    x_axis_title: str = (
        language_dict.get("forecast", {})
        .get(language_selection, {})
        .get("x_title_trend", "")
    )

    line = (
        alt.Chart(df)
        .mark_line(interpolate="basis", color="#624F82")
        .encode(
            x=alt.X(
                f"{x_field}:N",
                title=x_axis_title,
            ),
            y=alt.Y(
                f"{y_field}:Q",
                scale=alt.Scale(zero=False),
                title=y_axis_title,
            ),
        )
    )

    shared_elements = _provide_interactive_chart_elements(
        language_selection=language_selection,
        x_field=x_field,
        y_field=y_field,
        decimals=2,
        df=df,
        current_chart=line,
    )

    return alt.layer(
        line,
        shared_elements.get("selectors"),
        shared_elements.get("points"),
        shared_elements.get("rules"),
        shared_elements.get("text"),
    ).properties(width=800, height=300)

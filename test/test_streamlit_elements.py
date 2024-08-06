def test_app(provide_App):
    assert not provide_App.exception


def test_language_switch(provide_App, provide_config_from_env):
    assert provide_App.markdown[0].value == provide_config_from_env[1].get(
        "welcome_text"
    ).get("Ger").replace("\n", "")

    provide_App.radio(key="SELECT_language").set_value("  ").run()
    assert provide_App.markdown[0].value == provide_config_from_env[1].get(
        "welcome_text"
    ).get("Eng").replace("\n", "")


def test_Forecast_page(
    provide_Forecast_page, provide_config_from_env, provide_station_list_forecast
):
    language_dict = provide_config_from_env[1]
    assert not provide_Forecast_page.exception
    assert provide_Forecast_page.text[0].value == language_dict.get("forecast", {}).get(
        "Ger"
    ).get("please_choose")

    # Click through the lower buttons
    for gas_type in ("E10", "E5", "Diesel"):
        provide_Forecast_page.radio(key="SELECT_gas_type_forecast").set_value(
            gas_type
        ).run()
        assert not provide_Forecast_page.exception

    # Enter a station to check that forecasting works
    provide_Forecast_page.selectbox(key="SELECT_station").set_value(
        provide_station_list_forecast[0]
    ).run(timeout=30)
    assert not provide_Forecast_page.exception

    assert len(provide_Forecast_page.tabs) == 2


def test_Map_page(provide_Map_page):
    assert not provide_Map_page.exception

    # Click through the lower buttons
    for gas_type in ("E10", "E5", "Diesel"):
        provide_Map_page.radio(key="SELECT_gas_type_map").set_value(gas_type).run(
            timeout=60
        )
        assert not provide_Map_page.exception

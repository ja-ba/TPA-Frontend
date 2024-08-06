import os
from pathlib import Path

import pandas as pd
import pytest
from streamlit.testing.v1 import AppTest
from tpa_frontend.config_handler.load_configs import create_config_from_env
from tpa_frontend.config_handler.load_configs import create_Forecast
from tpa_frontend.config_handler.load_configs import create_PandasOCI_from_dict
from tpa_frontend.data_loader.load import loadBaseDFs


@pytest.fixture(scope="session")
def provide_config_path():
    path = "test/test_config.yaml"
    os.environ["CONFIG_PATH"] = path
    return path


@pytest.fixture(scope="session")
def provide_config_from_env(provide_config_path):
    return create_config_from_env()


@pytest.fixture(scope="session")
def provide_pandasOCI(provide_config_from_env):
    return create_PandasOCI_from_dict(configDict=provide_config_from_env[0])


@pytest.fixture(scope="session")
def provide_Forecast(provide_config_from_env):
    return create_Forecast(todays_date=provide_config_from_env[0]["todays_date"])


@pytest.fixture(scope="session")
def provide_App(provide_config_from_env):
    test_app = AppTest.from_file("../src/tpa_frontend/main.py")
    test_app.run(timeout=30)
    return test_app


@pytest.fixture(scope="session")
def provide_Forecast_page(provide_config_from_env):
    main_patched = Path("src/tpa_frontend/main.py").read_text()
    main_patched = main_patched.replace(
        "selectedSideBar=selectedSideBar", "selectedSideBar='forecast'"
    ).replace('selectedSideBar == "forecast"', "True")

    test_app = AppTest.from_string(main_patched)
    test_app.run(timeout=30)
    return test_app


@pytest.fixture(scope="session")
def provide_Map_page(provide_config_from_env):
    main_patched = Path("src/tpa_frontend/main.py").read_text()
    main_patched = main_patched.replace(
        "selectedSideBar=selectedSideBar", "selectedSideBar='maps'"
    ).replace('selectedSideBar == "maps"', "True")

    test_app = AppTest.from_string(main_patched)
    test_app.run(timeout=60)
    return test_app


@pytest.fixture(scope="session")
def provide_station_list_forecast(provide_config_from_env, provide_pandasOCI):
    base_df_dict = loadBaseDFs(
        config_dict=provide_config_from_env[0], _pandas_connection=provide_pandasOCI
    )
    return list(base_df_dict.get("station_info_30", pd.DataFrame())["Tankstellen_Name"])

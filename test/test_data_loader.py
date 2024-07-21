import pandas as pd
from tpa_frontend.data_loader.load import loadBaseDFs
from tpa_frontend.data_loader.load import makeForecast


class Test_load:
    def test_loadBaseDFs(self, provide_config_from_env, provide_pandasOCI):
        loaded_dfs = loadBaseDFs(
            config_dict=provide_config_from_env[0], _pandas_connection=provide_pandasOCI
        )

        assert isinstance(loaded_dfs, dict)
        for val in loaded_dfs.values():
            assert isinstance(val, pd.DataFrame)

    def test_makeForecast(self, provide_config_from_env, provide_Forecast):
        loaded_forecasts = makeForecast(
            config_dict=provide_config_from_env[0],
            station="13",
            gas_type="e10",
            _forecaster=provide_Forecast,
        )

        for val in loaded_forecasts.values():
            assert isinstance(val, pd.DataFrame)

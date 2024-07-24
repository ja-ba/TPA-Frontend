from datetime import date
from unittest.mock import patch

from cloud_storage_wrapper.oci_access.pandas import PandasOCI
from tpa_analytics_engine.api import Forecast
from tpa_frontend.config_handler.load_configs import create_config_from_env
from tpa_frontend.config_handler.load_configs import load_config_dict
from tpa_frontend.config_handler.load_configs import load_language_config_dict


class Test_load_configs:
    def test_load_config_dict(self, provide_config_path):
        todays_date = date.today()
        config_dict = load_config_dict(
            todays_date=todays_date, config_path=provide_config_path
        )
        assert config_dict["todays_date"] == todays_date
        assert "language_config" in config_dict

    def test_provide_pandasOCI(self, provide_pandasOCI):
        assert isinstance(provide_pandasOCI, PandasOCI)

    def test_provide_Forecast(self, provide_Forecast):
        assert isinstance(provide_Forecast, Forecast)

    def test_load_language_config_dict(self, provide_config_from_env):
        test_language_dict = load_language_config_dict(provide_config_from_env[0])

        assert isinstance(test_language_dict, dict)
        assert "welcome_text" in test_language_dict
        assert test_language_dict.get("welcome_text", {}).get(
            "Ger"
        ) == provide_config_from_env[1].get("welcome_text", {}).get("Ger")

    def test_create_config_from_env(self, provide_config_path, provide_config_from_env):
        with patch(
            "tpa_frontend.config_handler.load_configs.load_config_dict"
        ) as mock_load_config_dict:
            mock_load_config_dict.return_value = provide_config_from_env[0]
            create_config_from_env()
            mock_load_config_dict.assert_called_once_with(
                todays_date=date.today(), config_path=provide_config_path
            )

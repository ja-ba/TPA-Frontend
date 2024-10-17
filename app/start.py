from pathlib import Path

import requests  # type: ignore

conf_path = "configs"
if not Path(conf_path).exists():
    Path(conf_path).mkdir(parents=True)
    config_url = "https://raw.githubusercontent.com/ja-ba/TPA-Frontend/refs/heads/main/configs/config.yaml"
    language_content_url = "https://raw.githubusercontent.com/ja-ba/TPA-Frontend/refs/heads/main/configs/language_content.yaml"

    for c in (
        (config_url, f"{conf_path}/config.yaml"),
        (language_content_url, f"{conf_path}/language_content.yaml"),
    ):
        response = requests.get(c[0])
        if response.status_code == 200:
            Path(c[1]).write_bytes(response)
            print("YAML file downloaded and saved successfully")
        else:
            print("Failed to download YAML file")

from tpa_frontend import main  # noqa: E402

main.run_app()

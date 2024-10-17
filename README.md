# About the project
Gasprice forecaster is a tool to increase the transparency in the opaque German gas price market.

The tool helps you to save on gas by:
- Forecasting today's price curve for every gas station in Germany
- Providing insights into the daily, weekly and long-term price patterns of any German gas station
- Showing the cheapest gas stations on a map

## About this package
This repository contains the code for building the frontend as a python package. The can be run via Streamlit to produce a fully functioning frontend demonstrating the functionality of the backend.

# How to use
## Prerequisites:
* `Python>=3.9` installed
* Access key to the cloud storage in OCI

## Test:
1. Install the package alongside the test dependencies, for example: `python -m pip install -e '.[test]'`
2. Ensure having the access key to OCI cloud storage as a file `example_key.pem` in the test directory
3. Ensure that `test_config.yaml` and `test_language_content.yaml` exist in the test directory
4. Run the tests either in **tox** (command: `tox`) or **pytest** (command: `python -m pytest`):

## Running the package via Streamlit:
1. Install the latest version of the package from Github, for example `python -m pip install git+https://github.com/ja-ba/TPA-Frontend.git`
2. Ensure that the access key to OCI cloud storage is available as an environment variable named `OCI_KEY`
3. Run `python -m streamlit run https://github.com/ja-ba/TPA-Frontend/app/start.py` to start the Streamlit app from anywhere or `python -m streamlit run app/start.py` after cloning this repo

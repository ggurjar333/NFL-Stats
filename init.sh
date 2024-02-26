py -m venv .venv
pip install -r requirements.txt
dagster project from-example --example quickstart_etl --name loveofsports_nfl
cd loveofsports_nfl
pip install -e ".[dev]"
dagster dev
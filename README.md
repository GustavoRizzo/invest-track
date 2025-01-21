# invest-track

## Prerequisites

- [UV](https://github.com/astral-sh/uv)
- [Docker](https://www.docker.com/)
- [Make](https://www.gnu.org/software/make/)


## Prepare `.env` file

Make a copy from `.env.example` to `.env` file. Edit and adjust the file. After that, just need to load the environment
variables:

```shell
cp .env.example .env
vi .env
```

## Run aplication with Docker and Makefile

```shell
make up # production
make up-dev # development
```

On the first time running the application:

```shell
make setup
```

## Run application locally (without docker)

To create the local environment:

```shell
pyenv local && pyenv install
python3 -m venv venv
source venv/bin/activate
pip install pip --upgrade
pip install poetry
poetry install
```

to run the first time:

```shell
poetry task setup
```

## To load all Company data for you StockPosition
Run in the Django shell:

```shell
poetry run python manage.py shell
```

```python
# Load Company Data
from ativa_investimentos.scripts.load_all_company_info import main as load_all_company_info
load_all_company_info()
# Load Daily Stock History
from ativa_investimentos.scripts.load_all_daily_stock_history import main as load_all_daily_stock_history
start = '2018-01-01'
end = '2024-03-12'
load_all_daily_stock_history(start, end)
```
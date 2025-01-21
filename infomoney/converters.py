from datetime import datetime
from django.utils.timezone import now
import polars as pl


def convert_infomoney_high_low_to_df(api_data: dict) -> pl.DataFrame:

    # Column names corrected
    columns = [
        "name", "symbol", "date", "current_value", "var_day", "var_week", "var_month",
        "var_year", "var_12_months", "min", "max", "volume"
    ]

    assert 'aaData' in api_data, "aaData not found in api_data"
    data = api_data['aaData']
    assert len(data) > 0, "No data found in aaData"

    # Convert to Polars DataFrame
    df = pl.DataFrame(data, schema=columns, orient="row")

    # Convert columns to correct types
    df = convert_infomoney_high_low_df_types(df)

    return df


def convert_to_decimal(value):
    try:
        # Remove possíveis espaços e substitui vírgula por ponto
        value = value.strip().replace(',', '.')
        return float(value)
    except (ValueError, AttributeError):
        return None


def convert_to_date(date_str):
    try:
        # Converte dd/mm para dd/mm/yyyy usando o ano atual
        current_year = now().year  # Get the current year
        day, month = map(int, date_str.split('/'))
        return datetime(current_year, month, day)
    except (ValueError, AttributeError):
        return None


def convert_infomoney_high_low_df_types(df: pl.DataFrame) -> pl.DataFrame:
    # Assume que df é seu DataFrame Polars
    df = df.with_columns([
        # Converte a coluna date
        pl.col('date').map_elements(convert_to_date,
                                    return_dtype=pl.Datetime).alias('date'),

        # Converte colunas numéricas
        pl.col('current_value').map_elements(
            convert_to_decimal, return_dtype=pl.Float64).round(2).alias('current_value'),
        pl.col('var_12_months').map_elements(
            convert_to_decimal, return_dtype=pl.Float64).round(2).alias('var_12_months'),
        pl.col('min').map_elements(convert_to_decimal,
                                   return_dtype=pl.Float64).round(2).alias('min'),
        pl.col('max').map_elements(convert_to_decimal,
                                   return_dtype=pl.Float64).round(2).alias('max'),
        pl.col('volume').map_elements(
            convert_to_decimal, return_dtype=pl.Float64).round(2).alias('volume')
    ])
    return df

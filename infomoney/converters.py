from datetime import datetime
from django.utils.timezone import now
import polars as pl


def convert_high_low_dict_to_df(api_data: dict) -> pl.DataFrame:

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
    df = convert_high_low_df_types(df)

    return df


def convert_to_decimal(value):
    try:
        # Remove possíveis espaços e substitui vírgula por ponto
        value = value.strip().replace(',', '.')
        return float(value)
    except (ValueError, AttributeError):
        return None


def convert_to_date(date_str) -> datetime:
    # There are two possible date formats: dd/mm/yyyy or HHhMM
    has_h = '/' not in date_str
    if not has_h:
        try:
            # Converte dd/mm para dd/mm/yyyy usando o ano atual
            current_year = now().year  # Get the current year
            day, month = map(int, date_str.split('/'))
            return datetime(current_year, month, day)
        except (ValueError, AttributeError):
            raise ValueError(f"Invalid date: {date_str}")
    else:
        try:
            # Converte HHhMM para dd/mm/yyyy HH:MM
            return datetime(now().year, now().month, now().day, int(date_str[:2]), int(date_str[3:]))
        except (ValueError, AttributeError):
            raise ValueError(f"Invalid date: {date_str}")


def convert_high_low_df_types(df: pl.DataFrame) -> pl.DataFrame:
    # Assume que df é seu DataFrame Polars

    # Converte a coluna date
    df = df.with_columns(
        pl.col('date').map_elements(convert_to_date,
                                    return_dtype=pl.Datetime).alias('date')
    )

    # Converte a coluna current_value
    df = df.with_columns(
        pl.col('current_value').map_elements(
            convert_to_decimal, return_dtype=pl.Float64
        ).round(2).alias('current_value')
    )

    # Converte a coluna var_12_months
    df = df.with_columns(
        pl.col('var_12_months').map_elements(
            convert_to_decimal, return_dtype=pl.Float64
        ).round(2).alias('var_12_months')
    )

    # Converte a coluna min
    df = df.with_columns(
        pl.col('min').map_elements(
            convert_to_decimal, return_dtype=pl.Float64
        ).round(2).alias('min')
    )

    # Converte a coluna max
    df = df.with_columns(
        pl.col('max').map_elements(
            convert_to_decimal, return_dtype=pl.Float64
        ).round(2).alias('max')
    )

    # Converte a coluna volume
    df = df.with_columns(
        pl.col('volume').map_elements(
            convert_to_decimal, return_dtype=pl.Float64
        ).round(2).alias('volume')
    )
    return df


def convert_high_low_df_to_model(df: pl.DataFrame) -> list:
    from .models import HighLow
    # Covert df to list of dictionaries
    data = df.to_dicts()
    breakpoint()
    highlow_instances = []
    for row in data:
        highlow_instances.append(HighLow(**row))
    return highlow_instances

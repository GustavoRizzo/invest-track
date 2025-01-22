from datetime import datetime
from django.utils.timezone import now
import pandas as pd

from core.utils import convert_dict_nan_values_to_none, convert_to_decimal


def convert_high_low_dict_to_df(api_data: dict) -> pd.DataFrame:

    # Column names corrected
    columns = [
        "name", "symbol", "date", "current_value", "var_day", "var_week", "var_month",
        "var_year", "var_12_months", "min", "max", "volume"
    ]

    assert 'aaData' in api_data, "aaData not found in api_data"
    data = api_data['aaData']
    assert len(data) > 0, "No data found in aaData"

    # Convert to pandas DataFrame
    df = pd.DataFrame(data, columns=columns)

    # Convert columns to correct types
    df = convert_high_low_df_types(df)

    return df


def convert_to_date(date_str) -> datetime.date:
    # There are two possible date formats: dd/mm/yyyy or HHhMM
    has_h = '/' not in date_str
    if not has_h:
        try:
            # Converte dd/mm para dd/mm/yyyy usando o ano atual
            current_year = now().year  # Get the current year
            day, month = map(int, date_str.split('/'))
            return datetime(current_year, month, day).date()
        except (ValueError, AttributeError):
            raise ValueError(f"Invalid date: {date_str}")
    else:
        try:
            # Converte HHhMM para dd/mm/yyyy HH:MM
            return datetime(now().year, now().month, now().day, int(date_str[:2]), int(date_str[3:])).date()
        except (ValueError, AttributeError):
            raise ValueError(f"Invalid date: {date_str}")


def convert_high_low_df_types(df: pd.DataFrame) -> pd.DataFrame:
    # Assume que df é seu DataFrame pandas

    # Converte a coluna date
    df['date'] = df['date'].apply(convert_to_date)

    # Converte a coluna current_value
    df['current_value'] = df['current_value'].apply(convert_to_decimal).round(2)

    # Converte a coluna var_12_months
    df['var_12_months'] = df['var_12_months'].apply(convert_to_decimal).round(2)

    # Converte a coluna min
    df['min'] = df['min'].apply(convert_to_decimal).round(2)

    # Converte a coluna max
    df['max'] = df['max'].apply(convert_to_decimal).round(2)

    # Converte a coluna volume
    df['volume'] = df['volume'].apply(convert_to_decimal).round(2)

    return df

def convert_high_low_df_to_model(df: pd.DataFrame, save: bool = False) -> list:
    from .models import HighLow

    # Covert df to list of dictionaries
    data = df.to_dict(orient='records')

    # Clean Dict
    data = convert_dict_nan_values_to_none(data)

    highlow_instances = []
    for row in data:
        highlow_instances.append(HighLow(**row))
    if save:
        HighLow.objects.bulk_create(highlow_instances)
    return highlow_instances
import pandas as pd


def convert_to_decimal(value: str) -> float:
    try:
        # Remove possíveis espaços e substitui vírgula por ponto
        value = value.strip().replace(',', '.')
        return float(value)
    except (ValueError, AttributeError):
        return None

def convert_dict_nan_values_to_none(data: list[dict]) -> list[dict]:
    """ Recive a list of dictionaries and replace NaN values to None.
    """
    for record in data:
        for key, value in record.items():
            if pd.isna(value):  # Check if value is NaN
                record[key] = None
    return data

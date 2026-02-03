import math

import pandas as pd

REQUIRED_COLUMNS = [
    'Equipment Name',
    'Type',
    'Flowrate',
    'Pressure',
    'Temperature',
]


def _safe_mean(series: pd.Series):
    value = pd.to_numeric(series, errors='coerce').mean()
    if pd.isna(value) or (isinstance(value, float) and math.isnan(value)):
        return None
    return float(value)


def compute_chemviz_analytics(df: pd.DataFrame) -> dict:
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f'Missing required columns: {missing}')

    total_equipment = int(len(df))
    avg_flowrate = _safe_mean(df['Flowrate'])
    avg_pressure = _safe_mean(df['Pressure'])
    avg_temperature = _safe_mean(df['Temperature'])

    type_distribution = (
        df['Type']
        .astype(str)
        .value_counts(dropna=False)
        .to_dict()
    )

    return {
        'total_equipment': total_equipment,
        'avg_flowrate': avg_flowrate,
        'avg_pressure': avg_pressure,
        'avg_temperature': avg_temperature,
        'type_distribution': type_distribution,
    }

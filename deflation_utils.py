"""Deflation utilities for ECON 5200 labs."""

import pandas as pd


def deflate_series(nominal, cpi, base_year=2020):
    """Convert a nominal time series to real (constant-dollar) values.

    Parameters
    ----------
    nominal : pd.Series
        Nominal values indexed by date.
    cpi : pd.Series
        CPI values indexed by date, at the SAME frequency and with the SAME
        seasonal adjustment as `nominal`.
    base_year : int
        Year whose dollars to express values in. The base is that year's
        average CPI.

    Returns
    -------
    pd.Series
        Real values in base_year dollars, on the dates both inputs share,
        with no missing values.

    Raises
    ------
    ValueError
        If base_year is not present in the CPI index, or if the two series
        share no dates.
    """
    if not (cpi.index.year == base_year).any():
        raise ValueError(f"Base year {base_year} not found in CPI data.")

    base_cpi = cpi[cpi.index.year == base_year].mean()

    nominal = nominal.dropna()
    cpi = cpi.dropna()

    combined = pd.concat([nominal, cpi], axis=1, join="inner")
    if combined.empty:
        raise ValueError("nominal and cpi share no dates.")
    nominal = combined.iloc[:, 0]
    cpi = combined.iloc[:, 1]

    real = nominal / cpi * base_cpi
    return real


def profile_dataframe(data, unit_col="name", time_col="date"):
    """Describe the structure and completeness of a DataFrame.

    Parameters
    ----------
    data : pd.DataFrame
        Data in long format, one row per (unit, period).
    unit_col : str
        Column identifying the unit of observation (e.g. country).
    time_col : str
        Column identifying the time period.

    Returns
    -------
    dict
        shape, n_units, n_periods, structure ("panel", "time series" or
        "cross-sectional"), complete_units, balanced, and missing
        (percent of missing values in each column).
    """
    profile = {}
    profile["shape"] = data.shape

    profile["n_units"] = data[unit_col].nunique()
    profile["n_periods"] = data[time_col].nunique()

    if profile["n_units"] > 1 and profile["n_periods"] > 1:
        profile["structure"] = "panel"
    elif profile["n_periods"] > 1:
        profile["structure"] = "time series"
    else:
        profile["structure"] = "cross-sectional"

    periods_per_unit = data.groupby(unit_col)[time_col].nunique()
    complete = periods_per_unit[periods_per_unit == profile["n_periods"]]
    profile["complete_units"] = len(complete)
    profile["balanced"] = len(complete) == profile["n_units"]

    missing = {}
    for col in data.columns:
        missing[col] = round(data[col].isna().mean() * 100, 1)
    profile["missing"] = missing

    return profile
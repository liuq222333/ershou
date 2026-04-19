# coding:utf-8
import re
from datetime import datetime
from typing import Iterable, Optional

import numpy as np
import pandas as pd

_YEAR_RE = re.compile(r"(\d{4})")


def parse_year(value) -> Optional[int]:
    if value is None:
        return None
    if isinstance(value, (int, np.integer)):
        return int(value)
    if isinstance(value, float) and not np.isnan(value):
        return int(value)
    match = _YEAR_RE.search(str(value))
    return int(match.group(1)) if match else None


def vehicleage_to_age(values: Iterable, reference_year: Optional[int] = None) -> np.ndarray:
    ref = reference_year if reference_year is not None else datetime.now().year
    out = np.array([parse_year(v) for v in values], dtype=object)
    ages = np.array([ref - y if y is not None else np.nan for y in out], dtype=float)
    return ages


def age_series(series: pd.Series, reference_year: Optional[int] = None) -> pd.Series:
    return pd.Series(vehicleage_to_age(series.tolist(), reference_year), index=series.index)

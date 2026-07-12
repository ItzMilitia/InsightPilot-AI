from pathlib import Path

import pandas as pd
import pytest

from backend.engines.data_engine import DataEngine


engine = DataEngine()


def test_load_csv():
    df = engine.load_dataset("datasets/banking/bank_customers.csv")

    assert isinstance(df, pd.DataFrame)
    assert not df.empty


def test_invalid_source():

    with pytest.raises(Exception):
        engine.load_dataset(None)


def test_invalid_extension():

    with pytest.raises(Exception):
        engine.load_dataset("datasets/banking/sample.txt")
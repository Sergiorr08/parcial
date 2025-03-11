import pytest
import csv
import os
from lambda_parser.main import save_to_csv


def test_save_to_csv():
    test_data = [
        ["2025-03-10", "Chapinero", "$300,000,000", "1", "1", "40"]
    ]

    save_to_csv(test_data, "test_output.csv")
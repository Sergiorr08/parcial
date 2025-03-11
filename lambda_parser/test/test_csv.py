import pytest
import csv
import os
from main import save_to_csv

def test_save_to_csv():
    test_data = [
        {"FechaDescarga": "2025-03-10", "Barrio": "Chapinero", "Valor": "$300,000,000", "NumHabitaciones": "1", "NumBanos": "1", "mts2": "40"}
    ]
    save_to_csv("test_output.csv", test_data)

    with open("test_output.csv", newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)

    assert len(rows) == 1
    assert rows[0]["Barrio"] == "Chapinero"

    os.remove("test_output.csv")  # Limpieza después de la prueba

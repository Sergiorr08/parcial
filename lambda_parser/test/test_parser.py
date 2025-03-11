import pytest
from main import parse_html

def test_parse_html():
    test_html = """
    <html>
        <body>
            <div class="property">
                <span class="price">$300,000,000</span>
                <span class="neighborhood">Chapinero</span>
                <span class="rooms">1</span>
                <span class="bathrooms">1</span>
                <span class="size">40</span>
            </div>
        </body>
    </html>
    """
    parsed_data = parse_html(test_html)
    
    assert parsed_data[0]["Barrio"] == "Chapinero"
    assert parsed_data[0]["Valor"] == "$300,000,000"
    assert parsed_data[0]["NumHabitaciones"] == "1"
    assert parsed_data[0]["NumBanos"] == "1"
    assert parsed_data[0]["mts2"] == "40"

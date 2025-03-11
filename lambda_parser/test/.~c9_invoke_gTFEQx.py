import pytest
from lambda_parser.main import extract_data_from_html, process_html_file
from unittest.mock import patch, MagicMock

# HTML de prueba
HTML_SAMPLE = """
<html>
    <body>
        <div class="listing-item">
            <div class="neighborhood">Chapinero</div>
            <div class="price">$1,500,000</div>
            <div class="rooms">2</div>
            <div class="bathrooms">1</div>
            <div class="size">50m2</div>
        </div>
    </body>
</html>
"""

def test_extract_data_from_html():
    result = extract_data_from_html(HTML_SAMPLE)
    assert len(result) == 1
    assert result[0][1] == "Chapinero"
    assert result[0][2] == "$1,500,000"
    assert result[0][3] == "2"
    assert result[0][4] == "1"
    assert result[0][5] == "50m2"

@patch("lambda_parser.main.s3_client")
def test_process_html_file(mock_s3_client):
    # Simular respuesta de S3
    mock_s3_client.get_object.return_value = {
        "Body": MagicMock(read=MagicMock(return_value=HTML_SAMPLE.encode("utf-8")))
    }

    mock_s3_client.put_object.return_value = True
    
    # Llamar a la función con una clave de prueba
    process_html_file("landing-casas-804/test.html")

    # Verificar que get_object fue llamado con los argumentos correctos
    mock_s3_client.get_object.assert_called_once_with(Bucket="landing-casas-xxx", Key="landing-casas-804/test.html")

    # Verificar que put_object fue llamado correctamente
    mock_s3_client.put_object.assert_called_once()

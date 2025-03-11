import pytest
from unittest.mock import patch
from lambda_scraper.main import download_html

@patch("lambda_scraper.main.requests.get")
@patch("lambda_scraper.main.s3_client.put_object")  # ⬅️ Simula la subida a S3
def test_download_html(mock_put_object, mock_get):
    # Simular respuesta HTTP
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = "<html>Test HTML</html>"

    # Llamar a la función
    html_contents = download_html()

    # Verificar que la función retornó 10 páginas
    assert len(html_contents) == 10

    # Verificar que cada HTML descargado contiene "<html>" y "Test HTML"
    for html in html_contents:
        assert "<html>" in html
        assert "Test HTML" in html

    # Verificar que requests.get() se llamó 10 veces (una por página)
    assert mock_get.call_count == 10

    # Verificar que put_object() se llamó 10 veces (una por archivo subido)
    assert mock_put_object.call_count == 10

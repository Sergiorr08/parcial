import pytest
from unittest.mock import patch
from main import download_html

@patch("main.requests.get")
def test_download_html(mock_get):
    # Simular una respuesta HTTP
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = "<html>Test HTML</html>"

    html_content = download_html("https://example.com")
    
    assert "<html>" in html_content
    assert "Test HTML" in html_content

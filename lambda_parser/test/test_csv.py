import pytest
import boto3
from moto import mock_aws
from lambda_parser.main import save_to_csv
from io import StringIO

S3_BUCKET_OUTPUT = "test-bucket"

@pytest.fixture
def s3_mock():
    with mock_aws():  # Activa el mock para S3
        s3 = boto3.client("s3", region_name="us-east-1")
        s3.create_bucket(Bucket=S3_BUCKET_OUTPUT)

        # Configura credenciales ficticias en boto3 para evitar errores
        boto3.setup_default_session(
            aws_access_key_id="test",
            aws_secret_access_key="test",
            aws_session_token="test",
        )
        
        yield s3  # Devuelve el cliente S3 mockeado

def test_save_to_csv(s3_mock):
    test_data = [
        ["2025-03-10", "Chapinero", "$300,000,000", "1", "1", "40"]
    ]
    
    key = "test_output.csv"
    save_to_csv(test_data, key)

    # Verifica si el archivo fue subido
    response = s3_mock.get_object(Bucket=S3_BUCKET_OUTPUT, Key=key)
    csv_content = response["Body"].read().decode("utf-8")
    
    assert "2025-03-10,Chapinero,$300,000,000,1,1,40" in csv_content  # Verifica el contenido

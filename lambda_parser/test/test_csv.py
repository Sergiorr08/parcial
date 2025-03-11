import pytest
import boto3
from moto import mock_aws
from lambda_parser.main import save_to_csv

S3_BUCKET_OUTPUT = "test-bucket"

@pytest.fixture
def s3_mock():
    with mock_aws():  # Activa el mock de AWS
        # Crea el cliente de S3 dentro del mock
        s3 = boto3.client("s3", region_name="us-east-1")
        s3.create_bucket(Bucket=S3_BUCKET_OUTPUT)
        
        # Configura credenciales ficticias para evitar el error
        boto3.setup_default_session(
            aws_access_key_id="test",
            aws_secret_access_key="test",
            aws_session_token="test",
        )
        
        yield s3  # Retorna el cliente S3 mockeado

def test_save_to_csv(s3_mock):
    test_data = [
        ["2025-03-10", "Chapinero", "$300,000,000", "1", "1", "40"]
    ]
    save_to_csv(test_data, "test_output.csv")

    response = s3_mock.list_objects_v2(Bucket=S3_BUCKET_OUTPUT)
    assert "Contents" in response  # Verifica que el archivo fue subido

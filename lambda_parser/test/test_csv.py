import pytest
import boto3
from moto import mock_aws
from lambda_parser.main import save_to_csv

S3_BUCKET_OUTPUT = "test-bucket"

@pytest.fixture
def s3_mock():
    with mock_aws():  # <--- Cambia mock_s3() por mock_aws()
        s3 = boto3.client("s3", region_name="us-east-1")
        s3.create_bucket(Bucket=S3_BUCKET_OUTPUT)
        yield s3

def test_save_to_csv(s3_mock):
    test_data = [
        ["2025-03-10", "Chapinero", "$300,000,000", "1", "1", "40"]
    ]
    save_to_csv(test_data, "test_output.csv")

    response = s3_mock.list_objects_v2(Bucket=S3_BUCKET_OUTPUT)
    assert "Contents" in response  # Verifica que el archivo fue subido

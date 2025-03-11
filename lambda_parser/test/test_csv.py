import pytest
import boto3
from moto import mock_aws
from lambda_parser.main import save_to_csv
import os

S3_BUCKET_OUTPUT = "test-bucket"

@mock_aws
def test_save_to_csv():
    # Configurar credenciales de AWS para el mock
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"
    
    # Crear el bucket antes de la prueba
    s3 = boto3.client("s3", region_name="us-east-1")
    s3.create_bucket(Bucket=S3_BUCKET_OUTPUT)
    
    # Datos de prueba
    test_data = [
        ["2025-03-10", "Chapinero", "$300,000,000", "1", "1", "40"]
    ]
    
    key = "test_output.csv"
    
    # Llamar a la función que queremos probar
    save_to_csv(test_data, key)
    
    # Verificar si el archivo fue subido correctamente
    response = s3.get_object(Bucket=S3_BUCKET_OUTPUT, Key=key)
    csv_content = response["Body"].read().decode("utf-8")
    
    # Verificar el contenido del CSV
    assert "2025-03-10,Chapinero,$300,000,000,1,1,40" in csv_content
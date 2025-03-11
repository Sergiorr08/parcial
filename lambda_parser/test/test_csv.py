import pytest
import boto3
from moto import mock_aws
from unittest.mock import patch
import os
import sys
from importlib import reload
import lambda_parser.main

S3_BUCKET_OUTPUT = "test-bucket"

@mock_aws
def test_save_to_csv():
    # Configurar credenciales de AWS para el mock
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"
    
    # Cambiar la variable de entorno S3_BUCKET_OUTPUT
    os.environ["S3_BUCKET_OUTPUT"] = S3_BUCKET_OUTPUT
    
    # Recargar el módulo para que tome las nuevas variables de entorno
    reload(lambda_parser.main)
    
    # Crear el bucket de prueba
    s3 = boto3.client("s3", region_name="us-east-1")
    s3.create_bucket(Bucket=S3_BUCKET_OUTPUT)
    
    # Reemplazar el cliente global s3_client en el módulo
    lambda_parser.main.s3_client = s3
    
    # Datos de prueba
    test_data = [
        ["2025-03-10", "Chapinero", "$300,000,000", "1", "1", "40"]
    ]
    
    key = "test_output.csv"
    
    # Llamar a la función que queremos probar
    lambda_parser.main.save_to_csv(test_data, key)
    
    # Verificar si el archivo fue subido correctamente
    response = s3.get_object(Bucket=S3_BUCKET_OUTPUT, Key=key)
    csv_content = response["Body"].read().decode("utf-8")
    
    # Verificar el contenido del CSV
    assert "2025-03-10,Chapinero,$300,000,000,1,1,40" in csv_content
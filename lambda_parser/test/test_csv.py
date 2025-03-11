import pytest
import boto3
from moto import mock_aws
from lambda_parser.main import save_to_csv, S3_BUCKET_OUTPUT as ORIGINAL_BUCKET
import os
import builtins
import sys

# Guardar referencias a los módulos y funciones originales
original_import = builtins.__import__

S3_BUCKET_OUTPUT = "test-bucket"

# Esta función reemplazará al import original
def mock_import(name, *args, **kwargs):
    # Si intentamos importar boto3, devolvemos nuestro módulo modificado
    if name == 'boto3':
        mock_module = original_import(name, *args, **kwargs)
        
        # Guardar la función original
        original_client = mock_module.client
        
        # Reemplazar con nuestra función que devuelve nuestro cliente S3
        def mock_client(service_name, *args, **kwargs):
            if service_name == 's3':
                return s3_test_client
            return original_client(service_name, *args, **kwargs)
        
        # Reemplazar la función client
        mock_module.client = mock_client
        return mock_module
    
    # Para cualquier otro import, usar el import original
    return original_import(name, *args, **kwargs)

@mock_aws
def test_save_to_csv():
    # Configurar credenciales
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"
    
    # Crear cliente S3 real con moto
    global s3_test_client
    s3_test_client = boto3.client("s3", region_name="us-east-1")
    s3_test_client.create_bucket(Bucket=S3_BUCKET_OUTPUT)
    
    # Modificar el import
    builtins.__import__ = mock_import
    
    # Modificar el nombre del bucket en el módulo
    # Si S3_BUCKET_OUTPUT es importado en otros módulos, esto podría fallar
    sys.modules['lambda_parser.main'].S3_BUCKET_OUTPUT = S3_BUCKET_OUTPUT
    
    try:
        # Datos de prueba
        test_data = [
            ["2025-03-10", "Chapinero", "$300,000,000", "1", "1", "40"]
        ]
        
        key = "test_output.csv"
        
        # Llamar a la función
        save_to_csv(test_data, key)
        
        # Verificar
        response = s3_test_client.get_object(Bucket=S3_BUCKET_OUTPUT, Key=key)
        csv_content = response["Body"].read().decode("utf-8")
        
        assert "2025-03-10,Chapinero,$300,000,000,1,1,40" in csv_content
    
    finally:
        # Restaurar el import original
        builtins.__import__ = original_import
        # Restaurar el nombre del bucket
        sys.modules['lambda_parser.main'].S3_BUCKET_OUTPUT = ORIGINAL_BUCKET
import os
import requests
import boto3
from datetime import datetime

S3_BUCKET = os.getenv("S3_BUCKET", "landing-casas-804")
s3_client = boto3.client("s3")


def download_html(
        base_url="https://casas.mitula.com.co/apartaestudio/bogota/?page={}"):
    today = datetime.today().strftime('%Y-%m-%d')
    downloaded_html = []  # ⬅️ Lista para almacenar los HTML descargados

    for page in range(1, 11):  # Descarga las primeras 10 páginas
        url = base_url.format(page)
        response = requests.get(url)
        if response.status_code == 200:
            file_name = f"{today}_page_{page}.html"
            s3_path = f"{today}/{file_name}"
            s3_client.put_object(
                Bucket=S3_BUCKET,
                Key=s3_path,
                Body=response.text)
            downloaded_html.append(response.text)  # ⬅️ Agregar HTML a la lista
            print(f"Guardado: {s3_path}")
        else:
            print(f"Error descargando {url}")

    return downloaded_html  # ⬅️ Devolver la lista de HTML descargados
    else:
        print(f"Error descargando {url}")

    return downloaded_html  # ⬅️ Devolver la lista de HTML descargados


def lambda_handler(event, context):
    download_html()
    return {"statusCode": 200, "body": "Descarga completada"}

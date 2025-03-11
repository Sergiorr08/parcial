import os
import requests
import boto3
from datetime import datetime, timezone

S3_BUCKET = os.getenv("S3_BUCKET", "landing-casas-804")
s3_client = boto3.client("s3")


def download_html(base_url="https://casas.mitula.com.co/find?operationType=sell&geoId=mitula-CO-poblacion-0000014156&text=Bogot%C3%A1%2C++%28Cundinamarca%29", pages=10):
    today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    downloaded_html = []

    for page in range(1, pages + 1):
        url = f"{base_url}&page={page}"  # Agregamos el número de página a la URL
        response = requests.get(url, headers={"User-Agent":"Mozzila/5.0"})

        if response.status_code == 200:
            file_name = f"{today}_page_{page}.html"
            s3_path = f"{today}/{file_name}"
            s3_client.put_object(
                Bucket=S3_BUCKET,
                Key=s3_path,
                Body=response.text
            )
            downloaded_html.append(response.text)
            print(f"Guardado: {s3_path}")
        else:
            print(f"Error descargando {url}")

    return downloaded_html


def lambda_handler(event, context):
    download_html()
    return {"statusCode": 200, "body": "Descarga completada"}

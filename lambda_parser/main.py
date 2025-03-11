import os
import boto3
import csv
from bs4 import BeautifulSoup
from datetime import datetime

S3_BUCKET_INPUT = os.getenv("S3_BUCKET_INPUT", "landing-casas-804")
S3_BUCKET_OUTPUT = os.getenv("S3_BUCKET_OUTPUT", "casas-final-804")
s3_client = boto3.client("s3")

def extract_data_from_html(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    listings = []
    
    for listing in soup.select(".listing-item"):  # Ajustar el selector según la estructura real
        barrio = listing.select_one(".neighborhood").text if listing.select_one(".neighborhood") else "N/A"
        valor = listing.select_one(".price").text if listing.select_one(".price") else "N/A"
        habitaciones = listing.select_one(".rooms").text if listing.select_one(".rooms") else "N/A"
        banos = listing.select_one(".bathrooms").text if listing.select_one(".bathrooms") else "N/A"
        metros = listing.select_one(".size").text if listing.select_one(".size") else "N/A"
        
        listings.append([datetime.today().strftime('%Y-%m-%d'), barrio, valor, habitaciones, banos, metros])
    
    return listings

def process_html_file(key):
    response = s3_client.get_object(Bucket=S3_BUCKET_INPUT, Key=key)
    html_content = response["Body"].read().decode("utf-8")
    extracted_data = extract_data_from_html(html_content)
    
    output_key = key.replace("landing-casas-804", "casas-final-804").replace(".html", ".csv")
    csv_buffer = "FechaDescarga,Barrio,Valor,NumHabitaciones,NumBanos,mts2\n"
    
    for row in extracted_data:
        csv_buffer += ",".join(row) + "\n"
    
    s3_client.put_object(Bucket=S3_BUCKET_OUTPUT, Key=output_key, Body=csv_buffer)
    print(f"CSV guardado en: {output_key}")

def lambda_handler(event, context):
    for record in event["Records"]:
        key = record["s3"]["object"]["key"]
        process_html_file(key)
    return {"statusCode": 200, "body": "Procesamiento completado"}

def save_to_csv(data, key):
    csv_buffer = "FechaDescarga,Barrio,Valor,NumHabitaciones,NumBanos,mts2\n"
    for row in data:
        csv_buffer += ",".join(row) + "\n"

    s3_client.put_object(Bucket=S3_BUCKET_OUTPUT, Key=key, Body=csv_buffer)
    print(f"CSV guardado en: {key}")
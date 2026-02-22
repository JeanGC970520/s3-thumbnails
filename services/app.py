import io
import json
import logging
import os
import uuid

import boto3
from PIL import Image

s3 = boto3.client("s3", endpoint_url="http://localstack:4566")
dynamodb = boto3.client("dynamodb", endpoint_url="http://localstack:4566")

THUMBNAIL_SIZE = (128, 128)
THUMBNAIL_BUCKET_NAME = os.getenv("THUMBNAIL_BUCKET_NAME", "thumbnails")
METADATA_TABLE = os.getenv("METADATA_TABLE", "ThumbnailsMetadata")

# TODO: Verificar porque no se están mostrando los logs en la consola de LocalStack
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),  # Output to console
    ],
)


class Logger:
    @staticmethod
    def info(message):
        logging.info(message)

    @staticmethod
    def warning(message):
        logging.warning(message)

    @staticmethod
    def error(message):
        logging.error(message)


def lambda_handler(event, context):
    print("Procesando evento: " + json.dumps(event))
    Logger.info("Evento recibido: " + json.dumps(event))

    try:
        for record in event["Records"]:
            bucket = record["s3"]["bucket"]["name"]
            key = record["s3"]["object"]["key"]

            process_image(bucket, key)
            # Escribir metadata en DynamoDB
            write_metadata(bucket, key, {"processed": True})
    except Exception as e:
        write_metadata(bucket, key, {"processed": False, "error": str(e)})
        Logger.error("Error procesando el evento: " + str(e))
        return {"statusCode": 500, "body": "Error procesando la imagen"}

    return {"statusCode": 200, "body": "Thumbnail creada"}


def process_image(bucket, key):
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        image_content = response["Body"].read()

        image = Image.open(io.BytesIO(image_content))
        image.thumbnail(THUMBNAIL_SIZE)

        buffer = io.BytesIO()
        image.save(buffer, format="JPEG")
        buffer.seek(0)

        s3.put_object(
            Bucket=THUMBNAIL_BUCKET_NAME,
            Key=f"thumb-{key}",
            Body=buffer,
            ContentType="image/jpeg",
        )
    except Exception as e:
        Logger.error("Error procesando la imagen: " + str(e))


def write_metadata(bucket, key, metadata):
    try:
        dynamodb.put_item(
            TableName=METADATA_TABLE,
            Item={
                "id": {"S": str(uuid.uuid4())},
                "imageKey": {"S": key},
                "bucket": {"S": bucket},
                "metadata": {"S": json.dumps(metadata)},
            },
        )
    except Exception as e:
        Logger.error("Error escribiendo metadata: " + str(e))

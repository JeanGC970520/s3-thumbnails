import io
import json

import boto3
from PIL import Image

s3 = boto3.client("s3", endpoint_url="http://localstack:4566")

THUMBNAIL_SIZE = (128, 128)
DEST_BUCKET = "thumbnails"


def lambda_handler(event, context):
    print("Evento recibido:", json.dumps(event))

    for record in event["Records"]:
        bucket = record["s3"]["bucket"]["name"]
        key = record["s3"]["object"]["key"]

        response = s3.get_object(Bucket=bucket, Key=key)
        image_content = response["Body"].read()

        image = Image.open(io.BytesIO(image_content))
        image.thumbnail(THUMBNAIL_SIZE)

        buffer = io.BytesIO()
        image.save(buffer, format="JPEG")
        buffer.seek(0)

        s3.put_object(
            Bucket=DEST_BUCKET,
            Key=f"thumb-{key}",
            Body=buffer,
            ContentType="image/jpeg",
        )

    return {"statusCode": 200, "body": "Thumbnail creada"}

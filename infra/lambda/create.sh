# Crea la función Lambda "thumbnail-generator" con el código empaquetado en "services/function.zip"
awslocal lambda create-function \
    --function-name thumbnail-generator \
    --runtime python3.9 \
    --handler app.lambda_handler \
    --timeout 10 \
    --memory-size 256 \
    --role arn:aws:iam::000000000000:role/thumbnail-lambda-execution-role \
    --environment Variables="{THUMBNAIL_BUCKET_NAME=thumbnails, METADATA_TABLE=ThumbnailsMetadata}" \
    --zip-file fileb://services/function.zip

# Editar resource policy de la Lambda para permitir que el servicio S3 invoque la 
# función cuando se suba un nuevo objeto al bucket "landing-images"
awslocal lambda add-permission \
    --function-name thumbnail-generator \
    --action lambda:InvokeFunction \
    --statement-id s3-landing-images-trigger-statement \
    --principal s3.amazonaws.com \
    --source-arn arn:aws:s3:::landing-images

# Actualiza el código de la función
# awslocal lambda update-function-code \
#     --function-name thumbnail-generator \
#     --zip-file fileb://services/function.zip

# Crea los buckets "landing-images" para recibir las imagenes a procesar
# y "thumbnails" para depositar las miniaturas generadas por la función Lambda
awslocal s3 mb s3://landing-images
awslocal s3 mb s3://thumbnails

# Configura el bucket "landing-images" para que invoque la función Lambda "thumbnail-generator"
awslocal s3api put-bucket-notification-configuration --bucket landing-images --notification-configuration '{
    "LambdaFunctionConfigurations": [{
            "LambdaFunctionArn": "arn:aws:lambda:us-east-1:000000000000:function:thumbnail-generator",
            "Events": ["s3:ObjectCreated:*"]
        }]
    }'

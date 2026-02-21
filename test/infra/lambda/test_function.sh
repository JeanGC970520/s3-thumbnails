
# Inova la función a manera de prueba, simulando un evento de S3
awslocal lambda invoke \
    --function-name thumbnail-generator \
    --cli-binary-format raw-in-base64-out \
    --payload '{"Records":[{"s3":{"bucket":{"name":"landing-images"},"object":{"key":"foo.jpg"}}}]}' \
    /tmp/out.json && cat /tmp/out.json
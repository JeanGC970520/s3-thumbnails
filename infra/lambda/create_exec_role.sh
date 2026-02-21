
# Crea la política de IAM con los permisos necesarios para que la función Lambda 
# pueda acceder a los buckets S3 y escribir en CloudWatch Logs
awslocal iam create-policy \
    --policy-name thumbnail-lambda-policy \
    --policy-document file://infra/lambda/lambda-policy.json

# Crea el rol de ejecución para la función Lambda y adjunta una trust policy
# que permita a  Lambda asumir el rol
awslocal iam create-role \
    --role-name thumbnail-lambda-execution-role \
    --assume-role-policy-document file://infra/lambda/trust-policy.json

# Adjunta la política de permisos al rol de ejecución
awslocal iam attach-role-policy \
    --role-name thumbnail-lambda-execution-role \
    --policy-arn arn:aws:iam::000000000000:policy/thumbnail-lambda-policy

# Creates a DynamoDB table named 'ThumbnailsMetadata' for storing thumbnail metadata
# 
# Table Configuration:
# - Table Name: ThumbnailsMetadata
# - Partition Key: id (String type)
# - Provisioned Capacity: 5 read units, 5 write units
#
# Usage: Run this script to initialize the DynamoDB table in LocalStack
# Prerequisites: LocalStack must be running with DynamoDB service enabled
awslocal dynamodb create-table \
    --table-name ThumbnailsMetadata \
    --attribute-definitions AttributeName=id,AttributeType=S \
    --key-schema AttributeName=id,KeyType=HASH \
    --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5


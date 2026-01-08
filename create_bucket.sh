#!/bin/bash

# Script to create S3 bucket using CloudFormation

set -e  # Exit on error

# Disable AWS CLI pager
export AWS_PAGER=""

# Color codes for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

STACK_NAME="setzy-s3-bucket"
TEMPLATE_FILE="cfn/s3.yaml"

echo -e "${BLUE}Creating CloudFormation stack: ${STACK_NAME}${NC}"

# Create the stack
aws cloudformation create-stack \
  --stack-name ${STACK_NAME} \
  --template-body file://${TEMPLATE_FILE}

echo -e "${YELLOW}Waiting for stack creation to complete...${NC}"

# Wait for stack creation to complete
aws cloudformation wait stack-create-complete --stack-name ${STACK_NAME}

echo -e "${GREEN}✓ Stack created successfully!${NC}"
echo ""

# Get the bucket name
BUCKET_NAME=$(aws cloudformation describe-stacks \
  --stack-name ${STACK_NAME} \
  --query 'Stacks[0].Outputs[?OutputKey==`BucketName`].OutputValue' \
  --output text)

echo -e "${GREEN}Bucket Name: ${BUCKET_NAME}${NC}"
echo ""
echo -e "${BLUE}Add this to your .env file:${NC}"
echo "S3_BUCKET_NAME=${BUCKET_NAME}"

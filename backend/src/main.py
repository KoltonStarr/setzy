from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile
from mypy_boto3_s3 import S3Client
import boto3
import os

load_dotenv()
s3_bucket_name = os.getenv("S3_BUCKET_NAME")
app = FastAPI()

@app.post("/upload/")
async def upload_file(file: UploadFile):
    print(f"Filename: {file.filename}")
    print(f"content_type: {file.content_type}")
    print(f"file_size: {file.size}")

    s3_client: S3Client = boto3.client('s3')
    
    s3_client.upload_fileobj(
        Fileobj=file.file,
        Bucket=s3_bucket_name,
        Key=file.filename
    )

    return {"Status": 200}
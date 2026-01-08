from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, HTTPException
from mypy_boto3_s3 import S3Client
from supported_audio_types import SUPPORTED_AUDIO_TYPES 
import boto3
import os

load_dotenv()
s3_bucket_name = os.getenv("S3_BUCKET_NAME")
app = FastAPI()

@app.post("/upload", status_code=201)
async def upload_file(file: UploadFile):
    print(f"Filename: {file.filename}")
    print(f"content_type: {file.content_type}")
    print(f"file_size: {file.size}")

    if file.content_type not in SUPPORTED_AUDIO_TYPES:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    s3_client: S3Client = boto3.client('s3')

    try:
        s3_client.upload_fileobj(
            Fileobj=file.file,
            Bucket=s3_bucket_name,
            Key=file.filename
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"message": "success!"}
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile
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

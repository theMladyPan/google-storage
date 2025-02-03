from fastapi import FastAPI, UploadFile, File
from google.cloud import storage
import os
import dotenv
import logging

dotenv.load_dotenv()

log = logging.getLogger(__name__)
app = FastAPI()

# Load environment variables (set these in Cloud Run)
BUCKET_NAME = os.getenv("GCS_BUCKET_NAME")

# Initialize Google Cloud Storage client
storage_client = storage.Client()


@app.get("/")
def read_root():
    return {"message": "Cloud Run + FastAPI + GCS"}


@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    """Uploads a file to Google Cloud Storage."""
    try:
        bucket = storage_client.bucket(BUCKET_NAME)
        blob = bucket.blob(file.filename)

        # Upload the file
        blob.upload_from_string(await file.read(), content_type=file.content_type)

        public_url = blob.public_url

        return {"file_name": file.filename, "public_url": public_url, "download_url": f"/download/{file.filename}"}

    except Exception as e:
        return {"error": str(e)}


@app.get("/list/")
async def list_files():
    """Lists files in the Google Cloud Storage bucket."""
    try:
        bucket = storage_client.bucket(BUCKET_NAME)
        blobs = bucket.list_blobs()

        return {"files": [blob.name for blob in blobs]}

    except Exception as e:
        return {"error": str(e)}


@app.get("/download/{file_name}")
async def download_file(file_name: str):
    """Downloads a file from Google Cloud Storage."""
    try:
        bucket = storage_client.bucket(BUCKET_NAME)
        blob = bucket.blob(file_name)

        # Download the file
        file_contents = blob.download_as_bytes()

        return file_contents

    except Exception as e:
        return {"error": str(e)}

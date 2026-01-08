#!/bin/bash

# Script to upload a .wav file to the /upload endpoint
# Usage: ./run.sh [path_to_wav_file]

# Default to the Debra Ajayi.wav file in the current directory if no argument provided
WAV_FILE="${1:-Debra Ajayi.wav}"

# Check if the file exists
if [ ! -f "$WAV_FILE" ]; then
    echo "Error: File '$WAV_FILE' not found!"
    exit 1
fi

# Get the filename for the form field
FILENAME=$(basename "$WAV_FILE")

echo "Uploading $FILENAME to http://127.0.0.1:8000/upload..."

# Send POST request with the .wav file
curl -X POST \
  -F "file=@$WAV_FILE;type=audio/wav" \
  http://127.0.0.1:8000/upload

echo ""
echo "Upload complete!"

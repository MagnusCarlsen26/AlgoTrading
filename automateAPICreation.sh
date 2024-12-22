#!/bin/bash

BASE_PROJECT_NAME="yourbase"  # Keep it short to allow room for suffixes
NUM_PROJECTS=10               # Number of projects to create
OUTPUT_FILE="project_links.txt"  # File to save the project links

# Clear the output file before starting (optional, only if you want to clear the file at the start)
# > $OUTPUT_FILE

for i in $(seq 1 $NUM_PROJECTS); do
  # Generate a compliant project ID
  TIMESTAMP=$(date +%s | tail -c 6)  # Use the last 6 digits of the timestamp
  PROJECT_ID="${BASE_PROJECT_NAME}-${i}-${TIMESTAMP}"  # Ensure <30 chars
  PROJECT_NAME="${BASE_PROJECT_NAME}-${i}"

  echo "Creating project $PROJECT_NAME with ID $PROJECT_ID"

  # Create the project
  gcloud projects create $PROJECT_ID --name="$PROJECT_NAME"

  # Set the active project
  gcloud config set project $PROJECT_ID

  # Enable the YouTube API
  echo "Enabling YouTube API for $PROJECT_NAME"
  gcloud services enable youtube.googleapis.com

  echo "Enabled services for $PROJECT_NAME:"
  gcloud services list --enabled

  # Save the project link to the output file (appending)
  PROJECT_LINK="https://console.cloud.google.com/apis/credentials?authuser=0&project=${PROJECT_ID}"
  echo "$PROJECT_LINK" >> $OUTPUT_FILE
  echo "Saved project link: $PROJECT_LINK"
done

echo "All project links saved in $OUTPUT_FILE"

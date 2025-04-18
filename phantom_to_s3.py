import requests
import boto3
import json
import os

# Get environment variables
phantombuster_api_key = os.getenv("PHANTOMBUSTER_API_KEY")
phantom_agent_id = os.getenv("PHANTOM_AGENT_ID")
s3_bucket_name = os.getenv("S3_BUCKET_NAME")

# Initialize AWS S3 client
s3 = boto3.client('s3')

# Step 1: Get run data from PhantomBuster
run_url = f"https://api.phantombuster.com/api/v2/agent-output/{phantom_agent_id}"
headers = {
    "X-Phantombuster-Key-1": phantombuster_api_key
}

response = requests.get(run_url, headers=headers)
response_data = response.json()

if 'data' in response_data and 'output' in response_data['data']:
    download_url = response_data['data']['output']['downloadUrl']

    # Step 2: Download the output data
    output_data = requests.get(download_url).content

    # Step 3: Upload to S3
    file_name = f"phantombuster_{phantom_agent_id}.json"
    s3.put_object(
        Bucket=s3_bucket_name,
        Key=file_name,
        Body=output_data
    )

    print(f"Successfully uploaded to {file_name} in S3.")
else:
    print("Failed to get output data from PhantomBuster.")

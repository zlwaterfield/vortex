import os
import boto3
import requests
from botocore.exceptions import ClientError, NoCredentialsError
import mimetypes
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

LOCAL_DIRECTORY = './'
EXCLUDE_FILES = ['sync.py', '.DS_Store', '.gitignore', 'README.md', 'requirements.txt', '.env', 'LICENSE']
EXCLUDE_DIRS = ['.git', 'venv', '__pycache__'] 

def create_s3_resource():
    return boto3.resource(
        's3',
        endpoint_url=os.getenv('BUCKET_ENDPOINT_URL'),
        aws_access_key_id=os.getenv('ACCESS_KEY'),
        aws_secret_access_key=os.getenv('SECRET_KEY'),
        region_name='auto'
    )

def get_file_url(s3_file):
    return f"{os.getenv('BUCKET_CUSTOM_DOMAIN')}/{s3_file}"

def create_short_link(s3_file):
    file_url = get_file_url(s3_file)
    dub_url = "https://api.dub.co/links?projectSlug=zlwaterfield"
    payload = {
        "url": file_url,
        "domain": "zlw.is",
    }
    headers = {
        "Authorization": f"Bearer {os.getenv('DUB_API_KEY')}",
        "Content-Type": "application/json"
    }
    response = requests.request("POST", dub_url, json=payload, headers=headers)
    
    if response.status_code == 200:
        short_link = response.json().get('shortLink')
        print(f"Short link created: {short_link}")
    else:
        print(f"Failed to create short link for {file_url}: {response.text}")

def file_exists(s3, s3_file):
    try:
        s3.meta.client.head_object(Bucket=os.getenv('BUCKET_NAME'), Key=s3_file)
        return True  # The file exists
    except ClientError as e:
        # If the error code is 404, the object does not exist.
        if e.response['Error']['Code'] == '404':
            return False
        else:
            # Propagate other exceptions, such as 403 Forbidden
            raise

def upload_file(s3, local_file, s3_file):
    if file_exists(s3, s3_file):
        # print(f"File already exists, skipped: {s3_file}")
        return  # Skip this file if it already exists

    # Guess the MIME type of the file
    mime_type, _ = mimetypes.guess_type(local_file)
    if mime_type is None:
        mime_type = 'application/octet-stream'  # Use a binary stream type as fallback

    try:
        s3.Bucket(os.getenv('BUCKET_NAME')).upload_file(
            Filename=local_file,
            Key=s3_file,
            ExtraArgs={'ContentType': mime_type}
        )
        print(f"\nUploaded: {s3_file} with ContentType {mime_type}")
        if os.getenv('DUB_API_KEY'):
            create_short_link(s3_file)
        else:
            file_url = get_file_url(s3_file)
            print(f"File uploaded: {file_url}")
    except FileNotFoundError:
        print(f"Error: File not found: {local_file}")
    except NoCredentialsError:
        print("Error: Credentials not available")

def sync_files(s3):
    for root, dirs, files in os.walk(LOCAL_DIRECTORY):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for filename in files:
            if filename in EXCLUDE_FILES:
                continue  # Skip this file

            local_path = os.path.join(root, filename)
            relative_path = os.path.relpath(local_path, LOCAL_DIRECTORY)
            s3_path = relative_path

            upload_file(s3, local_path, s3_path)

def delete_extra_files(s3):
    bucket = s3.Bucket(os.getenv('BUCKET_NAME'))
    for obj in bucket.objects.all():
        s3_file = obj.key
        local_file = os.path.join(LOCAL_DIRECTORY, s3_file)

        if not os.path.exists(local_file):
            print(f"Deleting: {s3_file}")
            obj.delete()

def main():
    s3 = create_s3_resource()
    print(f"Syncing files from {LOCAL_DIRECTORY} to {os.getenv('BUCKET_NAME')}")
    sync_files(s3)
    print("\nDeleting extra files")
    delete_extra_files(s3)
    print("\nSync complete")

if __name__ == "__main__":
    main()

# TODO: get short link from path by searching Dub
# TODO: delete short link if file is deleted

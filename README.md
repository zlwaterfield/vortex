# Vortex

Vortex syncs files from a local directory to an Cloudflare R2 returns the hosted URL. Additionally, it generates short links for the uploaded files using the Dub API (optional).

## Features

- **File Synchronization**: Uploads all files from a local directory to an S3 bucket, excluding specified files.
- **Short Link Generation**: Generates short links for uploaded files using the Dub API.

## Prerequisites

- Python 3.8 or higher
- An Cloudflare account and R2 bucket (note: this would work with AWS S3 but isn't tested)
- (optional) Dub account with API key

## Installation

1. **Clone the repository**:
```bash
git clone https://github.com/zlwaterfield/vortex.git
cd vortex
```

2. **Create virtual environment and install dependencies**:
```bash
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. **Set up your `.env` file**:
Create a `.env` file in the root of the project with the following variables:
```
BUCKET_ENDPOINT_URL=<your_endpoint_url>
ACCESS_KEY=<your_access_key>
SECRET_KEY=<your_secret_key>
BUCKET_NAME=<your_bucket_name>
CUSTOM_DOMAIN=<your_custom_domain_for_short_links>
DUB_API_KEY=<your_dub_api_key> (optional)
```

## Usage

To run the script to synchronize your files to S3 and generate short links:
```bash
python sync.py
```

## Contributing

Contributions are welcome! For major changes, please open an issue first to discuss what you would like to change.

## License

Distributed under the MIT License. See `LICENSE` for more information.
```

This README template includes basic sections that describe what the script does, how to set it up, and how to run it. You can modify the repository URL and any other specifics to better fit your project's context.
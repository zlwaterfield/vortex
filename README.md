# Vortex

The goal of Vortex is to make it easy to host media files and share their links. Think of a self-hosted Google Drive.

Vortex syncs files from a local directory to a Cloudflare R2 bucket. It also generates short links for the uploaded files using the Dub API. This is all done via the terminal.

## Features

- **File Synchronization**: Sync files from a local directory to a Cloudflare R2 bucket
  - Upload new local files to the bucket
  - Delete files in the bucket that were deleted locally
- **Short Link Generation**: Generates short links for uploaded files using the Dub API

## Coming soon
- Auto delete short links for deleted files
- Update the documentation for S3 usage (Cloudflare R2 is S3 compatible)
- Make the custom domains more clear
- Add instructions on how to set up R2
- Delete the local file if deleted in bucket
- Hash file names instead of using them directly
- Show more examples and add images to the README
- Improve the CLI output and make it prettier
- Talk about solutions for generating media like Zappy
- Add UI for manage the files

## Prerequisites

- Python 3.8 or higher
- A Cloudflare account and R2 bucket (note: this would work with AWS S3 but isn't tested)
- (optional) Dub account with API key

## Installation

1. **Clone the repository**:
```bash
git clone https://github.com/zlwaterfield/vortex.git
cd vortex
```

2. **Create a virtual environment and install dependencies**:
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

4. **Start adding files**
Use the Vortex folder as your local hosting directory. Each file you add will be part of the next sync. It supports folders as well.

## Usage

Run the script to synchronize your local files to your R2 bucket and generate short links:
```bash
python sync.py
```

## Contributing

Contributions are welcome! For major changes, please open an issue first to discuss what you would like to change.

## License

Distributed under the MIT License. See `LICENSE` for more information.
```

This README template includes basic sections that describe what the script does, how to set it up, and how to run it. You can modify the repository URL and any other specifics to better fit your project's context.

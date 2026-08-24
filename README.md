# Flickr Photo Metadata Collector

A Python script based on the Flickr API. It searches for photos by keyword, retrieves image size, capture date, owner information, photo geolocation, and publicly available user location data, then stores the results in a SQLite database.

## Features

- Search Flickr photos by keyword
- Filter by capture date range, page size, and safe search
- Retrieve photo geotags and public user location/country data
- Retrieve the largest available image URL
- Store results in SQLite and update duplicate photo IDs automatically
- Retry automatically when Flickr API errors occur

## Requirements

- Python 3.9+
- A Flickr API key and secret

Install the dependency:

```bash
pip install flickrapi
```

## Configuration

Do not hard-code Flickr credentials in the source code or commit them to GitHub. Set the following environment variables before running the script.

macOS / Linux:

```bash
export FLICKR_API_KEY="your_api_key"
export FLICKR_API_SECRET="your_api_secret"
```

Windows PowerShell:

```powershell
$env:FLICKR_API_KEY = "your_api_key"
$env:FLICKR_API_SECRET = "your_api_secret"
```

You can optionally set `FLICKR_DB_FILE` to choose the database filename. The default is `flickr_yunnan3.db`.

## Usage

Edit `KEYWORDS`, `MIN_DATE`, and `MAX_DATE` near the top of `flickr_download.py`, then run:

```bash
python flickr_download.py
```

The script creates a SQLite database in the current directory. The main table is `photos`, with fields including photo ID, title, image URL, capture date, owner, coordinates, photo location, user location, and search keyword.

## Notes

- Follow Flickr's API terms of service, rate limits, and photo copyright requirements.
- The script stores image URLs and metadata returned by Flickr; it does not download image files automatically.
- The availability of photo and user location data depends on what Flickr users have made public.
- Large searches may generate many API requests and take a significant amount of time.

import os
import sqlite3
import time

import flickrapi


# Flickr API credentials should be provided through environment variables.
API_KEY = os.environ.get("FLICKR_API_KEY")
API_SECRET = os.environ.get("FLICKR_API_SECRET")
DB_FILE = os.environ.get("FLICKR_DB_FILE", "flickr_yunnan3.db")

KEYWORDS = ["China-Burma-India Theater"]
PER_PAGE = 100
MIN_DATE = "2005-01-01"
MAX_DATE = "2026-07-26"


def init_db(db_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS photos (
            id TEXT PRIMARY KEY, title TEXT, image_url TEXT, size_label TEXT,
            date_taken TEXT, owner_nsid TEXT, owner_name TEXT, flickr_page_url TEXT,
            latitude REAL, longitude REAL, photo_city TEXT, photo_country TEXT,
            user_location TEXT, user_country TEXT, search_keyword TEXT
        )
        """
    )
    conn.commit()
    print(f"Database '{db_file}' is ready.")
    return conn


def save_photo_to_db(conn, photo_data):
    conn.execute(
        """
        INSERT OR REPLACE INTO photos VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            photo_data["id"], photo_data["title"], photo_data["image_url"], photo_data["size_label"],
            photo_data["date_taken"], photo_data["owner_nsid"], photo_data["owner_name"],
            photo_data["flickr_page_url"], photo_data["latitude"], photo_data["longitude"],
            photo_data["photo_city"], photo_data["photo_country"], photo_data["user_location"],
            photo_data["user_country"], photo_data["search_keyword"],
        ),
    )


def fetch_photo_metadata(flickr, photo):
    photo_id = photo["id"]
    owner_nsid = photo.get("owner")
    owner_name = photo.get("ownername", "N/A")
    photo_city = photo_country = user_location = user_country = None

    if photo.get("latitude") not in (None, 0, "0"):
        try:
            info = flickr.photos.getInfo(photo_id=photo_id)["photo"]
            location = info.get("location", {})
            photo_city = location.get("locality", {}).get("_content")
            photo_country = location.get("country", {}).get("_content")
        except flickrapi.FlickrError:
            pass

    try:
        person = flickr.people.getInfo(user_id=owner_nsid)["person"]
        user_location = person.get("location", {}).get("_content")
        country_data = person.get("country")
        user_country = country_data.get("_content") if isinstance(country_data, dict) else country_data
    except flickrapi.FlickrError:
        pass

    try:
        sizes = flickr.photos.getSizes(photo_id=photo_id).get("sizes", {}).get("size", [])
        image_url, size_label = (sizes[-1]["source"], sizes[-1]["label"]) if sizes else (None, None)
    except flickrapi.FlickrError:
        return None

    if not image_url:
        return None

    return {
        "id": photo_id,
        "title": photo.get("title", "Untitled"),
        "image_url": image_url,
        "size_label": size_label,
        "date_taken": photo.get("datetaken"),
        "owner_nsid": owner_nsid,
        "owner_name": owner_name,
        "flickr_page_url": f"https://www.flickr.com/photos/{owner_nsid}/{photo_id}/",
        "latitude": photo.get("latitude"),
        "longitude": photo.get("longitude"),
        "photo_city": photo_city,
        "photo_country": photo_country,
        "user_location": user_location,
        "user_country": user_country,
        "search_keyword": "",
    }


def main():
    if not API_KEY or not API_SECRET:
        raise RuntimeError("请先设置 FLICKR_API_KEY 和 FLICKR_API_SECRET 环境变量。")

    conn = init_db(DB_FILE)
    flickr = flickrapi.FlickrAPI(API_KEY, API_SECRET, format="parsed-json")
    total_saved_count = 0

    try:
        for keyword in KEYWORDS:
            page_num = 1
            while True:
                try:
                    search_results = flickr.photos.search(
                        text=f'"{keyword}"', min_taken_date=MIN_DATE, max_taken_date=MAX_DATE,
                        per_page=PER_PAGE, safe_search=1, sort="date-taken-desc",
                        extras="date_taken, owner_name, geo", page=page_num,
                    )
                    photos_data = search_results["photos"]
                    photos = photos_data["photo"]
                    total_pages = photos_data["pages"]
                    if not photos:
                        break

                    print(f"Found {len(photos)} photo(s) on page {page_num}/{total_pages}.")
                    for photo in photos:
                        photo_details = fetch_photo_metadata(flickr, photo)
                        if photo_details:
                            photo_details["search_keyword"] = keyword
                            save_photo_to_db(conn, photo_details)
                            conn.commit()
                            total_saved_count += 1
                        time.sleep(1.2)

                    if page_num >= total_pages:
                        break
                    page_num += 1
                    time.sleep(2)
                except flickrapi.FlickrError as error:
                    print(f"Flickr API error: {error}; retrying in 60 seconds.")
                    time.sleep(60)
    finally:
        conn.close()
        print(f"Process complete. {total_saved_count} records saved to '{DB_FILE}'.")


if __name__ == "__main__":
    main()

"""
phish_in_tracks_downloader.py

A script to download all Phish tracks from phish.in within a specified date range (example: 1983–1989), using modern Python best practices and explanatory comments throughout.

Author: Your Name
Date: 2024-07-09

Software Development Best Practices covered:
- Modular, reusable functions (each function does one thing)
- Use of type hints for clarity
- Robust error handling
- Polite API usage (rate limiting)
- Configurable variables at the top
- Clear, beginner-friendly documentation
- Array/list concepts explained
- Minimal side effects
"""

import requests
import time
import json
from datetime import datetime
from typing import List, Dict

# ---------------------- CONFIGURATION ----------------------
# Change these values as needed
START_DATE = "1983-12-02"     # Beginning of date range (inclusive)
END_DATE = "1989-12-31"       # End of date range (inclusive)
SLEEP_BETWEEN_REQUESTS = 1    # Seconds to pause between requests (API politeness)
OUTPUT_FILE = "phish_1983_1989_tracks.json"
# ----------------------------------------------------------

def parse_date(date_str: str) -> datetime:
    """
    Convert a date string (YYYY-MM-DD) into a datetime object.
    This lets us compare dates easily and robustly.
    """
    return datetime.strptime(date_str, "%Y-%m-%d")

def get_phishnet_show_dates(start_date: str, end_date: str) -> List[str]:
    """
    Fetch all show dates from phish.net v3 API (no API key needed for setlists).
    Filter locally in Python for the date range.
    Returns a list of date strings (YYYY-MM-DD).
    """
    start = parse_date(start_date)
    end = parse_date(end_date)
    url = "https://api.phish.net/v3/setlists?format=json&limit=all"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    show_dates = []
    for show in data.get("data", []):
        date_str = show.get("showdate")
        if date_str:
            date_dt = parse_date(date_str)
            if start <= date_dt <= end:
                show_dates.append(date_str)
    return show_dates

def download_tracks_from_show_dates(show_dates: List[str]) -> List[Dict]:
    """
    For each show date, hit phish.in's /shows/{date} endpoint.
    Returns a combined list of all tracks for all shows on those dates.
    """
    all_tracks: List[Dict] = []
    for date_str in show_dates:
        url = f"https://phish.in/api/v2/shows/{date_str}"
        headers = {"Accept": "application/json"}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            tracks = data.get("tracks", [])
            if tracks:
                print(f"{date_str}: {len(tracks)} tracks found")
                all_tracks.extend(tracks)
        else:
            print(f"{date_str}: No show found on phish.in")
        time.sleep(SLEEP_BETWEEN_REQUESTS)
    return all_tracks

def save_tracks_to_file(tracks: List[Dict], filename: str) -> None:
    """
    Save the entire list (array) of tracks to a JSON file.
    JSON is a common format for structured data—human- and machine-readable.
    """
    with open(filename, "w") as f:
        json.dump(tracks, f, indent=2)

def main():
    """
    The main entry point for the script. Uses phish.net to fetch all known show dates for the range,
    then fetches tracks from phish.in for those dates and saves them to a file.
    """
    print(f"Fetching show dates from phish.net between {START_DATE} and {END_DATE}...")
    show_dates = get_phishnet_show_dates(START_DATE, END_DATE)
    print(f"Found {len(show_dates)} Phish show dates from phish.net.")
    tracks = download_tracks_from_show_dates(show_dates)
    save_tracks_to_file(tracks, OUTPUT_FILE)
    print(f"Done! {len(tracks)} tracks saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()


# ----------------------
# Glossary & Concepts:
# - List/Array: In Python, a 'list' is an ordered collection of items. It is similar to an array in other languages.
# - Dict/Dictionary: A mapping of key-value pairs (like a phone book). Each track is a dict with fields like 'title', 'show_date', etc.
# - yield: (not used here, but often in Python) - a keyword that lets a function return values one at a time, pausing after each, and resuming where it left off. See: https://realpython.com/introduction-to-python-generators/
# - API: A way for programs to talk to each other—here, we use HTTP requests to ask phish.in for track data.
# - JSON: A way to save complex structured data in a human-readable text file. Learn more: https://www.json.org/json-en.html
# ----------------------

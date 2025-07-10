import requests
import time
import json
from datetime import datetime, timedelta

# Helper to generate every date in 2024
start_date = datetime.strptime("2024-01-01", "%Y-%m-%d")
end_date = datetime.strptime("2024-12-31", "%Y-%m-%d")

def daterange(start_date, end_date):
    for n in range((end_date - start_date).days + 1):
        yield (start_date + timedelta(n)).strftime("%Y-%m-%d")

# Fetch all tracks for a given show date
def fetch_tracks_for_date(date_str):
    url = f"https://phish.in/api/v2/shows/{date_str}"
    headers = {"Accept": "application/json"}
    response = requests.get(url, headers=headers)
    if response.status_code == 404:
        return []  # No show that day
    response.raise_for_status()
    data = response.json()
    return data.get("tracks", [])

all_tracks = []

for date_str in daterange(start_date, end_date):
    tracks = fetch_tracks_for_date(date_str)
    if tracks:
        all_tracks.extend(tracks)
        print(f"Downloaded {len(tracks)} tracks from {date_str}")
    else:
        print(f"No show on {date_str}")
    time.sleep(1)  # Be polite!

# Save all tracks to a local JSON file
with open("phish_2024_tracks.json", "w") as f:
    json.dump(all_tracks, f, indent=2)

print(f"\nDone! Downloaded {len(all_tracks)} tracks total for 2024.")

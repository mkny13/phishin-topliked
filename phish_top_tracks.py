import requests
from datetime import datetime, timedelta

# Helper to generate all dates in the range (inclusive)
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

# Set your date range and likes threshold
start_date = datetime.strptime("1997-11-22", "%Y-%m-%d")
end_date = datetime.strptime("1997-12-31", "%Y-%m-%d")
likes_min = 10

# Collect tracks from all dates in range
all_tracks = []
for date_str in daterange(start_date, end_date):
    tracks = fetch_tracks_for_date(date_str)
    filtered = [t for t in tracks if t["likes_count"] >= likes_min]
    all_tracks.extend(filtered)

# Rank all tracks by likes, highest to lowest
ranked_tracks = sorted(all_tracks, key=lambda t: t["likes_count"], reverse=True)

# Print results
print(f"Tracks from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')} with likes >= {likes_min}:")
for i, t in enumerate(ranked_tracks, 1):
    print(f"{i}. {t['title']} ({t['show_date']}) — {t['likes_count']} likes")
    print(f"   MP3: {t['mp3_url']}")

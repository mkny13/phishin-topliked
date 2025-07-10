from phishin_queries import get_top_liked_tracks

db_url = "postgresql://localhost/phishin"  # Update with your username if needed
start_date = "2024-01-01"
end_date = "2025-01-01"
limit = 10

df = get_top_liked_tracks(db_url, start_date, end_date, limit)
print(df)

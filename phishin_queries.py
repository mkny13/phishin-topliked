# phishin_queries.py

import pandas as pd
from sqlalchemy import create_engine

def get_top_liked_tracks(
    db_url: str,
    start_date: str,
    end_date: str,
    limit: int = 50
) -> pd.DataFrame:
    sql = f"""
    SELECT lc.likes AS likes,
           t.id AS track_id,
           t.title,
           s.date,
           s.venue_name,
           tours.name AS tour_name
    FROM
      (SELECT count(*) likes,
              likable_id id
       FROM likes
       WHERE likable_type = 'Track'
       GROUP BY likable_id) lc
    INNER JOIN tracks AS t ON lc.id = t.id
    INNER JOIN shows AS s ON t.show_id = s.id
    INNER JOIN tours ON s.tour_id = tours.id
    WHERE s.date BETWEEN '{start_date}'::date AND '{end_date}'::date
    ORDER BY likes DESC
    LIMIT {limit}
    """
    engine = create_engine(db_url)
    df = pd.read_sql(sql, engine)
    return df


if __name__ == "__main__":
    db_url = "postgresql://localhost/phishin"
    start_date = "2024-01-01"
    end_date = "2025-01-01"
    limit = 10

    df = get_top_liked_tracks(db_url, start_date, end_date, limit)
    print(df)

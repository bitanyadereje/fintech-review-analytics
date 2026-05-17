import pandas as pd
import psycopg2

conn = psycopg2.connect(
    dbname="bank_reviews",
    user="postgres",
    password="postgres123",
    host="127.0.0.1",
    port=5434
)
cur = conn.cursor()

banks = [("CBE", "CBE Mobile"), ("BOA", "BOA Mobile"), ("Dashen", "Dashen Mobile")]
for name, app in banks:
    cur.execute("INSERT INTO banks (bank_name, app_name) VALUES (%s, %s) ON CONFLICT (bank_name) DO NOTHING", (name, app))
conn.commit()

cur.execute("SELECT bank_name, bank_id FROM banks")
bank_map = {name: bid for name, bid in cur.fetchall()}

df = pd.read_csv("data/reviews_with_themes.csv")
print(f"Loaded {len(df)} reviews")

insert_sql = """
    INSERT INTO reviews (bank_id, review_text, rating, review_date,
                         sentiment_label, sentiment_score, identified_theme, source)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
"""
for _, row in df.iterrows():
    cur.execute(insert_sql, (
        bank_map[row['bank']],
        row['review'],
        row['rating'],
        row['date'],
        row['sentiment_label'],
        row['sentiment_score'],
        row['theme'],
        row['source']
    ))

conn.commit()
print("Data inserted successfully.")

cur.execute("SELECT COUNT(*) FROM reviews")
print(f"Total reviews in DB: {cur.fetchone()[0]}")

cur.close()
conn.close()

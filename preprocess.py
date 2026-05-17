import pandas as pd

df = pd.read_csv("data/raw_reviews.csv")
initial = len(df)

dups = df.duplicated(subset=["review", "date", "bank"], keep=False)
df[dups].sort_values(by=["bank", "date", "review"])

# 1. Drop duplicates
df = df.drop_duplicates(subset=["review", "date", "bank"])
print(f"After dedup: {len(df)} rows (removed {initial - len(df)})")

# 2. Drop rows missing review or rating
df = df.dropna(subset=["review", "rating"])
print(f"After dropping nulls: {len(df)} rows")

# 3. Normalize date
df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")

# 4. Ensure rating is integer
df["rating"] = df["rating"].astype(int)

# Save cleaned CSV
df.to_csv("data/cleaned_reviews.csv", index=False)
print(f"\n✅ Cleaned data saved. Final shape: {df.shape}")
print(f"Reviews per bank:\n{df['bank'].value_counts()}")
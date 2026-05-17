import pandas as pd
from transformers import pipeline
from tqdm import tqdm


print("Loading sentiment model...")
sentiment_pipeline = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english"
)


df = pd.read_csv("data/cleaned_reviews.csv")
print(f"Analyzing {len(df)} reviews...")

# Function to get sentiment with safe handling of long texts
def get_sentiment(text):
    if not isinstance(text, str) or len(text.strip()) == 0:
        return "NEUTRAL", 0.0
    # Truncate to 512 tokens (model's max length)
    truncated = text[:512]
    result = sentiment_pipeline(truncated)[0]
    label = result['label']  # 'POSITIVE' or 'NEGATIVE'
    score = result['score']
    return label, score

# Apply with progress bar
tqdm.pandas()
df[['sentiment_label', 'sentiment_score']] = df['review'].progress_apply(
    lambda x: pd.Series(get_sentiment(x))
)

# (Optional) Add a neutral class if confidence is low
# Uncomment if you want three classes:
# df['sentiment_label'] = df.apply(
#     lambda row: 'NEUTRAL' if row['sentiment_score'] < 0.6 else row['sentiment_label'],
#     axis=1
# )

# Save results
df.to_csv("data/reviews_with_sentiment.csv", index=False)
print("\n✅ Sentiment analysis complete!")
print(df['sentiment_label'].value_counts())
print("\nSample:")
print(df[['review', 'sentiment_label', 'sentiment_score']].head())
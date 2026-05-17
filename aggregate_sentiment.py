import pandas as pd

df = pd.read_csv("data/reviews_with_sentiment.csv") 

agg= df.groupby(['bank', 'rating'])['sentiment_score'].mean().round(3)
print("Mean sentiment score by bank and rating:")
print(agg)


print("\nMean sentiment counts per bank:")
print(pd.crosstab(df['bank'], df['sentiment_label']))
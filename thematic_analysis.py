import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import re

df = pd.read_csv("data/reviews_with_sentiment.csv")

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'[^a-z\s]', '', text)
    return text

df['clean_review'] = df['review'].apply(clean_text)

banks = df['bank'].unique()
for bank in banks:
    bank_reviews = df[df['bank'] == bank]['clean_review'].tolist()
    if len(bank_reviews) < 10:
        print(f"{bank}: not enough reviews")
        continue
    
    vectorizer = TfidfVectorizer(stop_words='english', max_features=20)
    tfidf = vectorizer.fit_transform(bank_reviews)
    avg_scores = tfidf.mean(axis=0).A1
    words = vectorizer.get_feature_names_out()
    word_scores = sorted(zip(words, avg_scores), key=lambda x: x[1], reverse=True)[:10]
    
    print(f"\n{bank} top keywords:")
    for w, s in word_scores:
        print(f"  {w} ({s:.3f})")

theme_keywords = {
    "Performance": ["slow", "crash", "freeze", "lag", "hang"],
    "Login": ["login", "otp", "password", "verify", "access"],
    "Transfer": ["transfer", "send", "payment", "money", "transaction"],
    "UI": ["interface", "design", "beautiful", "easy", "simple"]
}

def assign_theme(text):
    text = str(text).lower()
    for theme, keywords in theme_keywords.items():
        if any(kw in text for kw in keywords):
            return theme
    return "Other"

df['theme'] = df['review'].apply(assign_theme)
df.to_csv("data/reviews_with_themes.csv", index=False)
print(df['theme'].value_counts())
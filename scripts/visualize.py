import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("data/reviews_with_themes.csv")

sentiment_counts = pd.crosstab(df['bank'], df['sentiment_label'])
sentiment_counts.plot(kind='bar', stacked=True, color=['#ff6b6b', "#94cf51"])
plt.title('Sentiment Distribution by Bank')
plt.ylabel('Number of Reviews')
plt.tight_layout()
plt.savefig('sentiment_by_bank.png')
plt.show()

plt.figure()
sns.boxplot(data=df, x='bank', y='rating')
plt.title('Rating Distribution per Bank')
plt.savefig('rating_boxplot.png')
plt.show()

theme_df = df[df['theme'] != 'Other']
theme_counts = theme_df.groupby(['bank', 'theme']).size().unstack(fill_value=0)
theme_counts.plot(kind='bar', stacked=True)
plt.title('Theme Frequency per Bank (excluding Other)')
plt.ylabel('Number of Reviews')
plt.legend(title='Theme', bbox_to_anchor=(1.05, 1))
plt.tight_layout()
plt.savefig('themes_by_bank.png')
plt.show()
# Fintech Review Analytics – Ethiopian Bank Mobile Apps

**Project for KAIM 9 – Week 2**  
*Scraping, sentiment & thematic analysis, PostgreSQL, and business insights*

---

## 📌 Overview

This project analyses user reviews of three Ethiopian banking apps:

- **Commercial Bank of Ethiopia (CBE)** – `com.combanketh.mobilebanking`
- **Bank of Abyssinia (BOA)** – `com.boa.boaMobileBanking`
- **Dashen Bank** – `com.cr2.amolelight`

We scraped 450+ reviews per bank (1,318 total), performed sentiment analysis using a transformer model (DistilBERT), extracted themes via TF‑IDF, stored everything in PostgreSQL, and produced actionable insights for product teams.

---

## 🗂️ Repository Structure
fintech-review-analytics/
├── .github/workflows/ # CI/CD (pytest on push)
├── .gitignore # ignores data/, *.csv, venv/
├── requirements.txt # Python dependencies
├── README.md # this file
├── data/ # CSV files (not committed)
├── scripts/ # all Python scripts
│ ├── scrape_full.py
│ ├── preprocess.py
│ ├── sentiment_analysis.py
│ ├── thematic_analysis.py
│ ├── aggregate_sentiment.py
│ ├── create_final_csv.py
│ ├── insert_db.py
│ └── schema.sql
└── 

## 🚀 Task 1 – Data Collection & Preprocessing

### Scraping

- Used `google-play-scraper` (Python library)
- Collected fields: `review`, `rating`, `date`, `bank`, `source`
- Target: 400+ reviews per bank – achieved:
  - CBE: 450
  - BOA: 450
  - Dashen: 450
- Date range: latest reviews available (May 2026)
- Saved raw data to `data/raw_reviews.csv` (not committed)

### Preprocessing

- Dropped exact duplicate reviews (based on review text + date + bank)
- Removed rows with missing `review` or `rating`
- Normalised dates to `YYYY-MM-DD`
- Saved cleaned data to `data/cleaned_reviews.csv`

**Output columns:** `review`, `rating`, `date`, `bank`, `source`

---

## 🧠 Task 2 – Sentiment & Thematic Analysis

### Sentiment Analysis

- Model: `distilbert-base-uncased-finetuned-sst-2-english` (Hugging Face)
- Each review classified as **POSITIVE** or **NEGATIVE** with a confidence score
- 1,318 reviews processed – 819 positive, 499 negative

**Aggregation results:**

| Bank   | NEGATIVE | POSITIVE |
|--------|----------|----------|
| CBE    | 143      | 283      |
| BOA    | 209      | 237      |
| Dashen | 147      | 299      |

### Thematic Analysis

- Cleaned text (lowercase, removed punctuation/emojis)
- Extracted top keywords per bank using **TF‑IDF**
- Grouped keywords into 4 business‑relevant themes:

| Theme       | Keywords                                 |
|-------------|------------------------------------------|
| Performance | slow, crash, freeze, lag, hang           |
| Login       | login, otp, password, verify, access     |
| Transfer    | transfer, send, payment, money, transaction |
| UI          | interface, design, beautiful, easy, simple |

- Reviews with no matching keywords → `Other`
- Saved final CSV: `data/final_analysis.csv` with columns:
  `review_id`, `review_text`, `sentiment_label`, `sentiment_score`, `identified_theme`


## 🗄️ Task 3 – PostgreSQL Database

### Schema

- **`banks`** table: `bank_id` (PK), `bank_name`, `app_name`
- **`reviews`** table: `review_id` (PK), `bank_id` (FK), `review_text`, `rating`, `review_date`, `sentiment_label`, `sentiment_score`, `identified_theme`, `source`

The schema is defined in `scripts/schema.sql`.

### Data Insertion

- Python script `insert_db.py` reads `data/reviews_with_themes.csv` and inserts rows into PostgreSQL.
- Connection parameters: localhost, port 5432, database `bank_reviews`, user `postgres`.
- Inserted **1,318 reviews** successfully.

### Verification Queries

```sql
SELECT COUNT(*) FROM reviews;                          -- 1318

SELECT b.bank_name, COUNT(r.review_id)
FROM reviews r JOIN banks b ON r.bank_id = b.bank_id
GROUP BY b.bank_name;


## Task 4 – Insights & Recommendations

### Visualizations

I created three plots to communicate key findings:

- `sentiment_by_bank.png` – stacked bar chart showing positive vs negative reviews per bank.
- `rating_boxplot.png` – boxplot of ratings (1–5) for each bank.
- `themes_by_bank.png` – stacked bar of theme frequencies (excluding generic "Other").

All plots have titles, labeled axes, and are referenced in the final report.

### Key Insights

**Satisfaction drivers** (from positive reviews):
- Easy UI, fast transfers, reliable OTP delivery.

**Pain points** (from negative reviews + themes):
- CBE: transfer delays, occasional crashes.
- BOA: login failures, confusing UI.
- Dashen: slow performance, OTP issues.

### Recommendations per Bank

- **CBE** – Optimise transfer backend; add transaction progress indicator.
- **BOA** – Simplify login flow; implement biometric fallback.
- **Dashen** – Improve crash recovery; promote Amole features with better onboarding.

### Final Report

The final report (`final_report.pdf`) is written in Medium‑blog style, ≤15 pages, with ≤15 plots. It includes:
- Executive summary
- Data collection & quality
- Sentiment & thematic analysis results
- Database design overview
- Insights, visualisations, bank‑specific recommendations
- Ethical considerations and limitations
- Next steps

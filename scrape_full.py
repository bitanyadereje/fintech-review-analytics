from google_play_scraper import reviews, Sort   # 👈 import Sort
import pandas as pd
import time

BANK_APPS = {
    "CBE": "com.combanketh.mobilebanking",
    "BOA": "com.boa.boaMobileBanking",
    "Dashen": "com.cr2.amolelight"
}

def scrape_bank(bank_name, app_id, target=450):
    print(f"\n📱 Scraping {bank_name}...")
    try:
        result, _ = reviews(
            app_id,
            lang='en',
            country='et',
            count=target,
            sort=Sort.NEWEST   # 👈 correct way
        )
        rows = []
        for r in result:
            rows.append({
                "review": r["content"],
                "rating": r["score"],
                "date": r["at"].date(),
                "bank": bank_name,
                "source": "Google Play"
            })
        print(f"   ✅ Got {len(rows)} reviews")
        return pd.DataFrame(rows)
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return pd.DataFrame()

all_dfs = []
for bank, app_id in BANK_APPS.items():
    df = scrape_bank(bank, app_id)
    if not df.empty:
        all_dfs.append(df)
    time.sleep(3)   # be nice to Google

if all_dfs:
    final_df = pd.concat(all_dfs, ignore_index=True)
    final_df.to_csv("data/raw_reviews.csv", index=False)
    print(f"\n🎉 Total reviews: {len(final_df)}")
    print(final_df['bank'].value_counts())
else:
    print("No data scraped. Check internet or app IDs.")
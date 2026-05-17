from google_play_scraper import reviews

apps = {
    "CBE": "com.combanketh.mobilebanking",
    "BOA": "com.boa.boaMobileBanking",
    "Dashen": "com.cr2.amolelight"
}

for bank, app_id in apps.items():
    try:
        result, _ = reviews(app_id, count=10)
        print(f"✓ {bank}: {len(result)} reviews found")
        if len(result) > 0:
            print(f"  Sample: {result[0]['content'][:80]}...\n")
    except Exception as e:
        print(f"✗ {bank}: Error - {e}\n")
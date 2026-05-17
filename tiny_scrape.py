from google_play_scraper import reviews

print("Testing with WhatsApp...")
result, _ = reviews("com.whatsapp", count=5, lang='en', country='us')
print(f"Got {len(result)} reviews")
for r in result:
    print(r['content'][:50])
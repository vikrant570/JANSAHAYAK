import re
import requests
from urllib.parse import urljoin

BASE_URL = "https://www.myscheme.gov.in/"
HTML_FILE = "data/raw/myscheme.html"

with open(HTML_FILE, "r", encoding="utf-8") as f:
    html = f.read()

script_urls = re.findall(
    r'<script[^>]+src=["\']([^"\']+)["\']',
    html,
    re.IGNORECASE
)

print("=" * 80)
print(f"FOUND {len(script_urls)} JAVASCRIPT FILES")
print("=" * 80)

for i, src in enumerate(script_urls, 1):

    url = urljoin(BASE_URL, src)

    print(f"\n[{i}] {url}")

    try:
        response = requests.get(
            url,
            timeout=30,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        print("STATUS:", response.status_code)

        if response.status_code != 200:
            continue

        js = response.text

        # Search for API-looking URLs
        patterns = [
            r'https?://[^"\']+',
            r'/api/[^"\']+',
            r'api/[^"\']+',
            r'graphql[^"\']*',
        ]

        matches = set()

        for pattern in patterns:
            found = re.findall(pattern, js, re.IGNORECASE)

            for item in found:
                matches.add(item)

        if matches:

            print("POSSIBLE API REFERENCES:")

            for item in sorted(matches):
                print("  ", item)

    except Exception as e:
        print("ERROR:", repr(e))
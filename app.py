from flask import Flask, render_template, request, jsonify
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin, urlparse

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/crawl', methods=['POST'])
def crawl():
    data = request.get_json()
    url = data.get('url')
    print(f"🔍 Crawling: {url}")

    if not url.startswith('http'):
        url = 'https://' + url

    try:
        r = requests.get(url, timeout=5)
        soup = BeautifulSoup(r.text, 'html.parser')
        base_url = f"{urlparse(url).scheme}://{urlparse(url).netloc}"

        links = []
        seen = set()

        for tag in soup.find_all('a', href=True):
            link = urljoin(base_url, tag['href'])
            if link in seen or not link.startswith('http'):
                continue
            seen.add(link)

            try:
                res = requests.get(link, timeout=3)
                inner = BeautifulSoup(res.text, 'html.parser')
                title = inner.title.string.strip() if inner.title else 'No title'

                domain = urlparse(link).netloc
                favicon = f"https://{domain}/favicon.ico"

                links.append({
                    'url': link,
                    'title': title,
                    'favicon': favicon
                })

                if len(links) >= 10:  # Optional limit
                    break

            except Exception as e:
                continue

        print(f"✅ Found {len(links)} links.")
        return jsonify({'links': links})

    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)

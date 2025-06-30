from flask import Flask, render_template, request, jsonify
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin, urlparse

app = Flask(__name__)

def extract_favicon(html, page_url):
    try:
        soup = BeautifulSoup(html, 'html.parser')
        icon_link = soup.find("link", rel=lambda x: x and "icon" in x.lower())
        if icon_link and icon_link.get("href"):
            return urljoin(page_url, icon_link["href"])
        # Fallback
        parsed = urlparse(page_url)
        return f"{parsed.scheme}://{parsed.netloc}/favicon.ico"
    except:
        return None

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
                inner_html = res.text
                inner_soup = BeautifulSoup(inner_html, 'html.parser')
                title = inner_soup.title.string.strip() if inner_soup.title else 'No title'

                favicon = extract_favicon(inner_html, link)

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

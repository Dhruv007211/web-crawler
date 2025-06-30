import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def crawl_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    links = []
    for a in soup.find_all('a', href=True):
        full_url = urljoin(url, a['href'])
        links.append(full_url)

    titles = [tag.get_text(strip=True) for tag in soup.find_all(['h1', 'h2', 'title'])]

    return {
        'links': links[:20],
        'titles': titles[:10]
    }

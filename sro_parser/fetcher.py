import requests

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/129.0.0.0 Safari/537.36"
    )
}


def build_page_url(url_template, page_number):
    if "{page}" not in url_template:
        return url_template
    return url_template.replace("{page}", str(page_number))


def fetch_html(url):
    response = requests.get(url, timeout=10, headers=headers)
    response.raise_for_status()
    return response.text

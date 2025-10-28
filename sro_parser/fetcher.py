import requests


def build_page_url(url_template, page_number):
    if "{page}" not in url_template:
        return url_template
    return url_template.replace("{page}", str(page_number))


def fetch_html(url):
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.text

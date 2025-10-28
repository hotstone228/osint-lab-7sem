from requests import RequestException

from sro_parser.config import PAGE_LIMIT, OUTPUT_FILE
from sro_parser.excel_writer import write_to_excel
from sro_parser.fetcher import build_page_url, fetch_html
from sro_parser.sources import SOURCES
from sro_parser.table_parser import parse_table


def iter_page_urls(url_template, page_limit):
    if "{page}" not in url_template:
        yield build_page_url(url_template, 1)
        return

    for page in range(1, page_limit + 1):
        yield build_page_url(url_template, page)


def collect_source(source, page_limit):
    url_template = source["url_template"]
    collected_rows = []
    headers = []

    for index, url in enumerate(iter_page_urls(url_template, page_limit), start=1):
        try:
            html = fetch_html(url)
        except RequestException as error:
            print("Не удалось загрузить", url, error)
            break

        page_headers, page_rows = parse_table(html)
        if page_headers and not headers:
            headers = page_headers

        if not page_rows:
            if index == 1:
                print("Не нашли таблицу на", url)
            break

        collected_rows.extend(page_rows)

        if "{page}" not in url_template:
            break

        if len(page_rows) == 0:
            break

    return headers, collected_rows


def run():
    datasets = []

    for source in SOURCES:
        print("Парсим", source["title"])
        headers, rows = collect_source(source, PAGE_LIMIT)
        if not rows:
            print("Пропускаем пустой источник", source["title"])
            continue

        datasets.append({
            "sheet": source["sheet"],
            "headers": headers,
            "rows": rows,
        })

    if not datasets:
        print("Не получилось собрать данные")
        return

    write_to_excel(datasets, OUTPUT_FILE)
    print("Сохранили файл", OUTPUT_FILE)

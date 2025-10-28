from bs4 import BeautifulSoup


def clean_text(text):
    return " ".join(text.split())


def parse_table(html):
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table")
    if not table:
        return [], []

    headers = []
    if table.thead:
        header_cells = table.thead.find_all("th")
        headers = [clean_text(cell.get_text(" ", strip=True)) for cell in header_cells]

    if not headers:
        first_row = table.find("tr")
        if first_row:
            cells = first_row.find_all(["th", "td"])
            headers = [clean_text(cell.get_text(" ", strip=True)) for cell in cells]
            data_rows = first_row.find_next_siblings("tr")
        else:
            data_rows = []
    else:
        body = table.tbody if table.tbody else table
        data_rows = body.find_all("tr")

    rows = []
    for row in data_rows:
        cells = row.find_all("td")
        if not cells:
            continue
        values = [clean_text(cell.get_text(" ", strip=True)) for cell in cells]
        if len(values) < len(headers):
            values.extend([""] * (len(headers) - len(values)))
        rows.append(values)

    return headers, rows

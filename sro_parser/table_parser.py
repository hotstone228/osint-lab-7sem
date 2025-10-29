from bs4 import BeautifulSoup


def clean_text(text):
    return " ".join(text.split())


def _expand_cells(cells):
    values = []
    for cell in cells:
        text = clean_text(cell.get_text(" ", strip=True))
        try:
            colspan = int(cell.get("colspan", 1))
        except (TypeError, ValueError):
            colspan = 1
        colspan = max(colspan, 1)
        values.append(text)
        if colspan > 1:
            values.extend([""] * (colspan - 1))
    return values


def _count_columns(row):
    total = 0
    for cell in row.find_all(["th", "td"]):
        try:
            colspan = int(cell.get("colspan", 1))
        except (TypeError, ValueError):
            colspan = 1
        total += max(colspan, 1)
    return total


def parse_table(html):
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table")
    if not table:
        return [], []

    headers = []
    data_rows = []

    if table.thead:
        header_cells = table.thead.find_all("th")
        headers = _expand_cells(header_cells)
        body = table.tbody if table.tbody else table
        data_rows = body.find_all("tr")
    else:
        all_rows = table.find_all("tr")
        if not all_rows:
            return [], []

        first_row = all_rows[0]
        header_cells = first_row.find_all("th")
        if header_cells:
            headers = _expand_cells(header_cells)
            data_rows = all_rows[1:]
        else:
            data_rows = all_rows
            max_columns = 0
            for row in data_rows:
                max_columns = max(max_columns, _count_columns(row))
            headers = [f"Column {i + 1}" for i in range(max_columns)]

    rows = []
    for row in data_rows:
        if row.find_parent("thead"):
            continue
        cells = row.find_all("td")
        if not cells:
            continue
        values = _expand_cells(cells)
        if len(values) < len(headers):
            values.extend([""] * (len(headers) - len(values)))
        rows.append(values[: len(headers)])

    return headers, rows

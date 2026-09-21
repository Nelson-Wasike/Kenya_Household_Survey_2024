"""
parser.py -Parser for KNBS Kenya Housing Survey 2024 report tables.
Turns report tables (merged cells, multi-row headers,
embedded Kenya/Rural/Urban summary rows, footnotes) into tidy data.
"""
import openpyxl
import sys
sys.path.insert(0, "D:/Projects/Kenya_Housing_Survey/khs/src")
from counties import KENYA_COUNTIES, normalize_county

RESIDENCE_LABELS = {"Kenya", "Rural", "Urban", "National"}
SECTION_MARKERS = {"County", "Counties", "Region"}

def read_raw_rows(filepath, sheetname):
    wb = openpyxl.load_workbook(filepath, data_only=True)
    ws = wb[sheetname]
    return list(ws.iter_rows(values_only=True))


def is_footnote_row(row):
    first = row[0]
    if first is None:
        return False
    text = str(first).strip().lower()
    return text.startswith(("source", "note", "*", "n/a", "n.b", "key:", "n =", "n="))


def is_blank_row(row):
    return all(c is None for c in row)


def find_county_start(rows):
    for i, row in enumerate(rows):
        val = normalize_county(row[0])
        if val in KENYA_COUNTIES:
            return i
    return None


def forward_fill_leading_columns(rows, n_cols_to_fill):
    filled = [list(r) for r in rows]
    last_vals = [None] * n_cols_to_fill
    for row in filled:
        for c in range(n_cols_to_fill):
            if row[c] is None:
                row[c] = last_vals[c]
            else:
                last_vals[c] = row[c]
    return filled


def detect_category_cols(rows, county_start, max_check=8):
    sample = rows[county_start:county_start + 100]
    n_cols = len(rows[county_start]) if rows[county_start] else 0
    category_cols = 0
    for c in range(1, min(n_cols, max_check)):
        col_vals = [r[c] for r in sample if len(r) > c and r[c] is not None]
        if not col_vals:
            continue
        if all(isinstance(v, str) for v in col_vals):
            category_cols += 1
        else:
            break
    return category_cols


def find_paired_block_offset(rows, county_start):
    sample = rows[county_start:county_start + 10]
    n_cols = max(len(r) for r in sample)
    for c in range(1, n_cols):
        hits = 0
        for r in sample:
            if len(r) > c and normalize_county(r[c]) in KENYA_COUNTIES:
                hits += 1
        if hits >= len(sample) - 1:
            return c
    return None


def parse_simple_table(filepath, sheetname):
    rows = read_raw_rows(filepath, sheetname)
    title = rows[0][0] if rows else None
    if len(rows) < 2:
        return [], {"title": title, "sheet": sheetname, "status": "EMPTY"}

    header = [h if h is not None else f"col_{i+1}" for i, h in enumerate(rows[1])]
    data_rows = rows[2:]
    end_idx = len(data_rows)
    for i, r in enumerate(data_rows):
        if is_footnote_row(r):
            end_idx = i
            break
    data_rows = [r for r in data_rows[:end_idx] if not is_blank_row(r)]

    tidy = []
    for row in data_rows:
        if row[0] is None:
            continue
        record = {}
        for h, v in zip(header, row):
            record[str(h).strip()] = v
        tidy.append(record)

    qc = {"title": title, "sheet": sheetname, "status": "OK" if tidy else "EMPTY",
          "rows_parsed": len(tidy), "kind": "national_or_reference"}
    return tidy, qc


def parse_county_table(filepath, sheetname, category_cols=0, value_col_names=None):
    rows = read_raw_rows(filepath, sheetname)
    title = rows[0][0] if rows else None

    county_start = find_county_start(rows)
    qc = {"title": title, "sheet": sheetname, "county_start": county_start}
    if county_start is None:
        qc["status"] = "NO_COUNTY_ROWS_FOUND"
        return [], qc

    header_end = county_start
    for i in range(1, county_start):
        first = rows[i][0]
        if first is not None and str(first).strip() in (RESIDENCE_LABELS | SECTION_MARKERS):
            header_end = i
            break
    header_rows = rows[1:header_end]

    data_rows = rows[county_start:]
    end_idx = len(data_rows)
    for i, r in enumerate(data_rows):
        if is_footnote_row(r):
            end_idx = i
            break
    data_rows = data_rows[:end_idx]
    data_rows = [r for r in data_rows if not is_blank_row(r)]

    def extract_block(block_rows, n_category_cols, names):
        filled = forward_fill_leading_columns(block_rows, 1 + n_category_cols)
        out = []
        matched = set()
        for row in filled:
            county = normalize_county(row[0])
            if county not in KENYA_COUNTIES:
                continue
            values = row[1 + n_category_cols:]
            if all(v is None for v in values):
                continue
            matched.add(county)
            record = {"county": county}
            for c in range(n_category_cols):
                record[f"category_{c+1}"] = row[1 + c]
            if names:
                for name, v in zip(names, values):
                    record[name] = v
            else:
                for j, v in enumerate(values):
                    record[f"value_{j+1}"] = v
            out.append(record)
        return out, matched

    pair_offset = find_paired_block_offset(rows, county_start)
    if pair_offset:
        block1 = [r[:pair_offset] for r in data_rows]
        block2 = [r[pair_offset:] for r in data_rows]
        tidy1, m1 = extract_block(block1, category_cols, value_col_names)
        tidy2, m2 = extract_block(block2, category_cols, value_col_names)
        tidy = tidy1 + tidy2
        matched_counties = m1 | m2
        qc["paired_layout"] = True
    else:
        tidy, matched_counties = extract_block(data_rows, category_cols, value_col_names)
        qc["paired_layout"] = False

    qc["counties_matched"] = len(matched_counties)
    qc["counties_expected"] = 47
    qc["rows_parsed"] = len(tidy)
    qc["header_rows"] = header_rows
    qc["status"] = "OK" if len(matched_counties) >= 40 else "LOW_COUNTY_MATCH"
    return tidy, qc

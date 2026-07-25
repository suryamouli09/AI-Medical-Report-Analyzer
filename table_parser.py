import pdfplumber
import pandas as pd
import re
import io
from analyzer import find_best_parameter_match

# ─────────────────────────────────────────────
# Extract Tables from PDF
# ─────────────────────────────────────────────

def clean_cell_text(text):
    if text is None:
        return ""
    text = str(text)
    # Remove null bytes and non-printable control characters
    text = re.sub(r'[\x00-\x1F\x7F-\x9F]', '', text)
    # Remove unreadable CID font glyph tags like (cid:123)
    text = re.sub(r'\(?cid:\d+\)?', '', text, flags=re.IGNORECASE)
    return text.strip()

def extract_tables_from_pdf(pdf_source):

    extracted_tables = []

    try:

        if isinstance(pdf_source, bytes):

            pdf_source = io.BytesIO(pdf_source)

        with pdfplumber.open(pdf_source) as pdf:

            for page in pdf.pages:

                tables = page.extract_tables()

                for table in tables:

                    if table:

                        cleaned_table = []

                        for row in table:

                            cleaned_row = [clean_cell_text(cell) for cell in row]

                            if any(cleaned_row):

                                cleaned_table.append(cleaned_row)

                        if cleaned_table:

                            df = pd.DataFrame(cleaned_table)

                            df = df.dropna(how="all").dropna(how="all", axis=1)

                            # Ignore tables filled only with non-alphanumeric noise
                            raw_str = " ".join(df.astype(str).values.flatten())

                            if len(re.findall(r'[A-Za-z0-9]', raw_str)) >= 3:

                                extracted_tables.append(df)

    except Exception as e:

        print("Table extraction error:", e)

    return extracted_tables


# ─────────────────────────────────────────────
# Convert Tables to Parameters
# ─────────────────────────────────────────────

def extract_parameters_from_tables(tables):

    parameters = {}

    for df in tables:

        for row in df.values:

            row_text = " ".join(
                [str(x) for x in row if x and str(x).strip()]
            )

            if not row_text:
                continue

            matched_param = find_best_parameter_match(row_text)

            if not matched_param:
                continue

            values = re.findall(r'\d+\.?\d*', row_text)

            if not values:
                continue

            for val in values:

                try:

                    num = float(val)

                    if 0 < num <= 1000000:

                        parameters[matched_param] = num

                        break

                except Exception:

                    pass

    return parameters
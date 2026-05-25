import pdfplumber
import pandas as pd
import re

# ─────────────────────────────────────────────
# Extract Tables from PDF
# ─────────────────────────────────────────────

def extract_tables_from_pdf(pdf_path):

    extracted_tables = []

    try:

        with pdfplumber.open(pdf_path) as pdf:

            for page in pdf.pages:

                tables = page.extract_tables()

                for table in tables:

                    if table:

                        df = pd.DataFrame(table)

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
                [str(x) for x in row if x]
            )

            # Extract parameter + value
            match = re.findall(
                r'([A-Za-z /()+%-]+)\s+(\d+\.?\d*)',
                row_text
            )

            for param, value in match:

                param = param.strip()

                try:
                    parameters[param] = float(value)

                except:
                    pass

    return parameters
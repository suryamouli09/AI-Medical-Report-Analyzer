import re

# ─────────────────────────────────────────────
# HIPAA-Compliant PII Data Privacy Shield
# ─────────────────────────────────────────────

def redact_pii(text):
    if not text or not isinstance(text, str):
        return text

    sanitized = text

    # 1. Phone Numbers
    sanitized = re.sub(
        r'\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b',
        '[PHONE REDACTED]',
        sanitized
    )

    # 2. Email Addresses
    sanitized = re.sub(
        r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b',
        '[EMAIL REDACTED]',
        sanitized
    )

    # 3. Social Security & National IDs (SSN / Aadhaar / National ID)
    sanitized = re.sub(
        r'\b\d{3}-\d{2}-\d{4}\b',
        '[SSN REDACTED]',
        sanitized
    )
    sanitized = re.sub(
        r'\b\d{4}\s?\d{4}\s?\d{4}\b',
        '[NATIONAL ID REDACTED]',
        sanitized
    )

    # 4. Lab Specimen / Accession / PID IDs
    sanitized = re.sub(
        r'\b(?:Specimen|Accession|Lab ID|Order ID|PID|MRN)[\s#:]*([A-Za-z0-9-]+)\b',
        r'\1: [ID REDACTED]',
        sanitized,
        flags=re.IGNORECASE
    )

    return sanitized

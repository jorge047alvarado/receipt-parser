import re

# ==========================================================
# HEADER
# ==========================================================

PURCHASE_DATE_RE = re.compile(
    r"^(?P<date>\d{2}/\d{2}/\d{2})\s+(?P<time>\d{2}:\d{2})$"
)

TRANSACTION_ID_RE = re.compile(
    r"^(?P<transaction_id>TC.?(?:\s+\d+)+)$",
    re.IGNORECASE,
)

# ==========================================================
# RECEIPT TOTALS
# ==========================================================

SUBTOTAL_RE = re.compile(
    r"""
    ^
    SUBTOTAL
    \s+
    (?P<subtotal>\d+\.\d{2})
    $
    """,
    re.VERBOSE,
)

TOTAL_RE = re.compile(
    r"""
    ^
    TOTAL
    \s+
    (?P<total>\d+\.\d{2})
    $
    """,
    re.VERBOSE,
)

# ==========================================================
# CHANGE DUE
# ==========================================================

CHANGE_RE = re.compile(
    r"""
    ^
    CHANGE\s+DUE
    \s+
    (?P<change>\d+\.\d{2})
    $
    """,
    re.VERBOSE,
)
# ==========================================================
# TAX
# ==========================================================

# Examples:
#
# TAX 1 10.5 % 21.09
# 1% TAX 2 4.46
# 6% TAX 4 0.30
#
# OCR can produce several variants.

TAX_RE = re.compile(
    r"""
    ^
    (?:
        TAX
        \s+(?P<code>\d+)
        \s+(?P<rate>\d+(?:\.\d+)?)
        \s*%
    )

    \s+

    (?P<amount>\d+\.\d{2})

    $
    """,
    re.VERBOSE,
)

ITEM_HEADER_RE = re.compile(
    r"""
    ^
    (?P<barcode>\d{10,11})
    \s+
    (?P<description>[A-Z0-9&'/().\- ]+)
    $
    """,
    re.VERBOSE,
)

# ==========================================================
# NORMAL ITEM
# ==========================================================

# Examples:
#
# 0980170727 MMBROCCHEDS 10.98
# 0980078905 GUINEOS MAD 2.82 R
# 0990532573 GLAZED DONU 5.17 T

ITEM_RE = re.compile(
    r"""
    ^
    (?P<barcode>\d{10,11})
    \s+
    (?P<description>[A-Z0-9&'/().\- ]+?)
    \s+
    (?P<price>\d+\.\d{2})
    (?:\s+(?P<item_code>[A-Z]))?
    $
    """,
    re.VERBOSE,
)

# ==========================================================
# MULTIBUY
# ==========================================================

# Examples:
#
# 2 AT 1 FOR 4.97 9.94 R
# 3 AT 1 FOR 5.57 16.71 Y
# 2 AT 1 FOR 58.87 117.74 T

MULTIBUY_RE = re.compile(
    r"""
    ^
    (?P<quantity>\d+)
    \s+AT\s+1\s+FOR\s+
    (?P<unit_price>\d+\.\d{2})
    \s+
    (?P<total_price>\d+\.\d{2})
    (?:\s+(?P<item_code>[A-Z]))?
    $
    """,
    re.IGNORECASE | re.VERBOSE,
)

# ==========================================================
# INSTANT SAVINGS
# ==========================================================

# Examples:
#
# INST SV COCOA PEBBL
# 2 AT 1 FOR 6.00- 12.00-T
# INST SV DEGREE MEN 3.00-T

DISCOUNT_HEADER_RE = re.compile(
    r"^INST\s+SV\s+(?P<description>.+)$",
    re.IGNORECASE,
)

MULTIBUY_HEADER_RE = re.compile(
    r"""
    ^
    (?P<barcode>\d{10,11})
    \s+
    (?P<description>[A-Z0-9&'/().\- ]+)
    $
    """,
    re.VERBOSE,
)

DISCOUNT_RE = re.compile(
    r"""
    ^
    INST\s+SV
    \s+
    (?P<description>.+?)
    \s+
    (?P<discount>\d+\.\d{2})
    -.*
    $
    """,
    re.VERBOSE,
)

DISCOUNT_INCOMPLETE_RE = re.compile(
    r"""
    ^
    (?P<discount>\d+\.\d{2})
    -
    (?P<suffix>.*)
    $
    """,
    re.VERBOSE,
)

MULTIBUY_DISCOUNT_RE = re.compile(
    r"""
    ^
    \d+
    \s+AT\s+\d+\s+FOR
    \s+
    \d+\.\d{2}-
    \s+
    (?P<discount>\d+\.\d{2})
    -.*
    $
    """,
    re.VERBOSE,
)

DATE_TIME_RE = re.compile(
    r"""
    ^
    (?P<date>\d{2}/\d{2}/\d{2})
    \s+
    (?P<time>\d{2}:\d{2})
    $
    """,
    re.VERBOSE,
)

CASH_REWARDS_RE = re.compile(
    r"""
    ^
    (?P<description>CASH\s+REWARDS\s+TEND)
    \s+
    (?P<amount>\d+\.\d{2})
    $
    """,
    re.VERBOSE | re.IGNORECASE,
)
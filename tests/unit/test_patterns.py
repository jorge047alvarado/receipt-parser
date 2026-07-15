import pytest

from src import patterns


@pytest.mark.unit
def test_purchase_date_pattern():
    match = patterns.PURCHASE_DATE_RE.match(
        "07/11/26 14:30"
    )

    assert match
    assert match.group("date") == "07/11/26"
    assert match.group("time") == "14:30"


@pytest.mark.unit
def test_transaction_id_pattern():
    match = patterns.TRANSACTION_ID_RE.match(
        "TC 123 456"
    )

    assert match
    assert match.group("transaction_id") == "TC 123 456"

@pytest.mark.unit
def test_subtotal_pattern():
    match = patterns.SUBTOTAL_RE.match(
        "SUBTOTAL 25.50"
    )

    assert match
    assert match.group("subtotal") == "25.50"


@pytest.mark.unit
def test_total_pattern():
    match = patterns.TOTAL_RE.match(
        "TOTAL 30.00"
    )

    assert match
    assert match.group("total") == "30.00"


@pytest.mark.unit
def test_change_pattern():
    match = patterns.CHANGE_RE.match(
        "CHANGE DUE 5.00"
    )

    assert match
    assert match.group("change") == "5.00"


@pytest.mark.unit
def test_tax_pattern():
    match = patterns.TAX_RE.match(
        "TAX 1 10.5 % 21.09"
    )

    assert match
    assert match.group("code") == "1"
    assert match.group("rate") == "10.5"
    assert match.group("amount") == "21.09"


@pytest.mark.unit
def test_item_header_pattern():
    match = patterns.ITEM_HEADER_RE.match(
        "0980170727 MMBROCCHEDS"
    )

    assert match
    assert match.group("barcode") == "0980170727"


@pytest.mark.unit
def test_item_pattern():
    match = patterns.ITEM_RE.match(
        "0980170727 MMBROCCHEDS 10.98 R"
    )

    assert match
    assert match.group("barcode") == "0980170727"
    assert match.group("price") == "10.98"
    assert match.group("item_code") == "R"


@pytest.mark.unit
def test_multibuy_pattern():
    match = patterns.MULTIBUY_RE.match(
        "2 AT 1 FOR 4.97 9.94 R"
    )

    assert match
    assert match.group("quantity") == "2"
    assert match.group("unit_price") == "4.97"
    assert match.group("total_price") == "9.94"


@pytest.mark.unit
def test_discount_patterns():
    match = patterns.DISCOUNT_HEADER_RE.match(
        "INST SV COCOA PEBBL"
    )

    assert match
    assert match.group("description") == "COCOA PEBBL"


@pytest.mark.unit
def test_discount_pattern():
    match = patterns.DISCOUNT_RE.match(
        "INST SV DEGREE MEN 3.00-T"
    )

    assert match
    assert match.group("discount") == "3.00"


@pytest.mark.unit
def test_incomplete_discount_pattern():
    match = patterns.DISCOUNT_INCOMPLETE_RE.match(
        "3.00-T"
    )

    assert match
    assert match.group("discount") == "3.00"


@pytest.mark.unit
def test_multibuy_discount_pattern():
    match = patterns.MULTIBUY_DISCOUNT_RE.match(
        "2 AT 1 FOR 6.00- 12.00-T"
    )

    assert match
    assert match.group("discount") == "12.00"


@pytest.mark.unit
def test_date_time_pattern():
    match = patterns.DATE_TIME_RE.match(
        "07/11/26 14:30"
    )

    assert match
    assert match.group("date") == "07/11/26"


@pytest.mark.unit
def test_cash_rewards_pattern():
    match = patterns.CASH_REWARDS_RE.match(
        "CASH REWARDS TEND 5.00"
    )

    assert match
    assert match.group("amount") == "5.00"
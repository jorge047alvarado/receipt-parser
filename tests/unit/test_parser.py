import pytest

from src.parser import ReceiptParser


@pytest.mark.unit
def test_parse_basic_receipt():

    parser = ReceiptParser()

    lines = [
        "SAM'S CLUB",
        "07/11/26 14:30",
        "TC 123456",
        "0980170727 MILK 5.99",
        "SUBTOTAL 5.99",
        "TAX 1 10.5 % 0.63",
        "TOTAL 6.62",
    ]

    receipt = parser.parse(lines)

    assert receipt.store == "SAM'S CLUB"
    assert receipt.purchase_date == "07/11/26"
    assert receipt.purchase_time == "14:30"
    assert receipt.transaction_id == "TC 123456"

    assert len(receipt.items) == 1
    assert receipt.items[0].description == "MILK"

    assert receipt.subtotal == 5.99
    assert receipt.total == 6.62

    assert len(receipt.taxes) == 1

@pytest.mark.unit
def test_parse_ignores_empty_lines():

    receipt = ReceiptParser().parse(
        [
            "",
            "   ",
            "TOTAL 10.00",
        ]
    )

    assert receipt.total == 10.00

@pytest.mark.unit
def test_parse_store_with_city():

    receipt = ReceiptParser().parse(
        [
            "SAM'S CLUB",
            "MAYAGUEZ, PR",
        ]
    )

    assert receipt.store == "SAM'S CLUB MAYAGUEZ, PR"

@pytest.mark.unit
def test_parse_multibuy_item():

    receipt = ReceiptParser().parse(
        [
            "0980170727 COFFEE",
            "2 AT 1 FOR 4.97 9.94 R",
        ]
    )

    item = receipt.items[0]

    assert item.quantity == 2
    assert item.unit_price == 4.97
    assert item.total_price == 9.94
    assert item.tax_code == "R"

@pytest.mark.unit
def test_parse_cash_rewards():

    receipt = ReceiptParser().parse(
        [
            "CASH REWARDS TEND 1.00",
        ]
    )

    assert receipt.cash_rewards == -1.00

    assert len(receipt.items) == 1
    assert receipt.items[0].item_type == "cash_rewards"

@pytest.mark.unit
def test_parse_multiple_taxes():

    receipt = ReceiptParser().parse(
        [
            "TAX 1 10.5 % 0.50",
            "TAX 2 6 % 0.30",
        ]
    )

    assert len(receipt.taxes) == 2
    assert receipt.tax_total == 0.80

@pytest.mark.unit
def test_parse_discount():

    receipt = ReceiptParser().parse(
        [
            "0980170727 COCOA PEBBL 5.00",
            "INST SV COCOA PEBBL 1.25-",
        ]
    )

    assert receipt.items[0].discount == -1.25

@pytest.mark.unit
def test_parse_discount_2():

    receipt = ReceiptParser().parse(
        ["SAM'S CLUB",
        "07/11/26 14:30",
        "TC 123456",
        "0980170727 COCOA PEBBL 5.00 T",
        "INST SV COCOA PEBBL",
        "1.25-T",
        "SUBTOTAL 5.00"
        ]
    )

    print(receipt.items)

    assert receipt.items[0].discount == -1.25
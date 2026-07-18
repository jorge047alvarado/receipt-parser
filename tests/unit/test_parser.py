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
    assert item.item_code == "R"

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

@pytest.mark.unit
def test_parse_discount_2():

    receipt = ReceiptParser().parse(
        ["sam's club",
         "TM","CLUB MANAGER JUAN",
         "7878052100",
         "MAYAGUEZ, PR",
         "07/05/26 15:02 4750 6225 83",
         "0990006012 DEGREE IS S 12.98 T",
         "INST SV DEGREE IS S",
         "3.00-T",

        ]
    )

    assert receipt.items[0].discount == -3.00

@pytest.mark.unit
def test_missed_line_for_discount_1():

    receipt = ReceiptParser().parse(["sam's club",
         "TM","CLUB MANAGER JUAN",
         "7878052100",
         "MAYAGUEZ, PR",
         "07/05/26 15:02 4750 6225 83",
         "0990006012 DEGREE IS S 12.98 T",
         "INST SV DEGREE IS S",
         "3.00-T",
         "INST SV DEGREE NOT THIS IS S",
        ])
    
    print(receipt)
    
    assert receipt.items[1].barcode == 0
    assert receipt.items[1].description == "INST SV DEGREE NOT THIS IS S"
    assert receipt.items[1].quantity == 0
    assert receipt.items[1].unit_price == 0
    assert receipt.items[1].total_price == 0
    assert receipt.items[1].discount == 0
    assert receipt.items[1].item_code == 'Z'
    assert receipt.items[1].item_type == 'MISSED-ITEM-AND-DISCOUNT'

@pytest.mark.unit

def test_complete_single_discount_line():

    receipt = ReceiptParser().parse(
        ["sam's club",
         "TM","CLUB MANAGER JUAN",
         "7878052100",
         "MAYAGUEZ, PR",
         "07/05/26 15:02 4750 6225 83",
         "0990006012 DEGREE IS S 12.98 T",
         "INST SV DEGREE IS S 7.00-T"
        ]
    )

    assert receipt.items[0].barcode == '0990006012'
    assert receipt.items[0].description == 'DEGREE IS S'
    assert receipt.items[0].quantity == 1
    assert receipt.items[0].unit_price == 12.98
    assert receipt.items[0].total_price == 12.98
    assert receipt.items[0].item_code == 'T'
    assert receipt.items[0].discount == -7.00

@pytest.mark.unit

def test_complete_single_line_item():

    receipt = ReceiptParser().parse(
        ["sam's club",
         "TM","CLUB MANAGER JUAN",
         "7878052100",
         "MAYAGUEZ, PR",
         "07/05/26 15:02 4750 6225 83",
         "0990006012 DEGREE IS S 12.98 T"
        ]
    )

    assert receipt.items[0].barcode == '0990006012'
    assert receipt.items[0].description == 'DEGREE IS S'
    assert receipt.items[0].quantity == 1
    assert receipt.items[0].unit_price == 12.98
    assert receipt.items[0].total_price == 12.98
    assert receipt.items[0].item_code == 'T'
    assert receipt.items[0].discount == 0.00

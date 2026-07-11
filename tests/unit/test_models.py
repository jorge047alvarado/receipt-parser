import pytest

from src.models import Receipt, ReceiptItem, TaxItem


@pytest.mark.unit
def test_receipt_item_final_price():
    item = ReceiptItem(
        total_price=10.00,
        discount=-2.00,
    )

    assert item.final_price == 8.00


@pytest.mark.unit
def test_receipt_item_properties():
    merchandise = ReceiptItem(item_type="item")
    tax = ReceiptItem(item_type="tax")

    assert merchandise.is_merchandise is True
    assert merchandise.is_tax is False

    assert tax.is_tax is True
    assert tax.is_merchandise is False


@pytest.mark.unit
def test_receipt_item_discount_property():
    discounted = ReceiptItem(discount=-1.00)
    normal = ReceiptItem(discount=0.00)

    assert discounted.is_discounted is True
    assert normal.is_discounted is False


@pytest.mark.unit
def test_receipt_item_to_dict():
    item = ReceiptItem(
        description="Milk",
        total_price=5.00,
        discount=-1.00,
    )

    result = item.to_dict()

    assert result["description"] == "Milk"
    assert result["final_price"] == 4.00


@pytest.mark.unit
def test_receipt_add_item_and_tax():
    receipt = Receipt()

    item = ReceiptItem(description="Bread")
    tax = TaxItem(
        tax_code="A",
        tax_rate=0.10,
        tax_amount=0.50,
    )

    receipt.add_item(item)
    receipt.add_tax(tax)

    assert receipt.items == [item]
    assert receipt.taxes == [tax]

@pytest.mark.unit
def test_receipt_tax_and_item_categories():
    receipt = Receipt()

    merchandise = ReceiptItem(
        description="Bread",
        total_price=5.00,
        discount=-1.00,
        item_type="item",
    )

    tax_line = ReceiptItem(
        description="Tax line",
        total_price=0.50,
        item_type="tax",
    )

    receipt.add_item(merchandise)
    receipt.add_item(tax_line)

    assert receipt.merchandise_items == [merchandise]
    assert receipt.tax_items == [tax_line]


@pytest.mark.unit
def test_receipt_calculated_values():
    receipt = Receipt()

    receipt.add_item(
        ReceiptItem(
            description="Milk",
            total_price=4.00,
            discount=-0.50,
        )
    )

    receipt.add_tax(
        TaxItem(
            tax_code="A",
            tax_rate=0.10,
            tax_amount=0.35,
        )
    )

    assert receipt.total_discount == -0.50
    assert receipt.calculated_subtotal == 3.50
    assert receipt.calculated_tax == 0.35
    assert receipt.calculated_total == 3.85


@pytest.mark.unit
def test_receipt_to_dict():
    receipt = Receipt(
        store="Sam's Club",
        subtotal=10.00,
        total=10.50,
        validation=["OK"],
    )

    receipt.add_tax(
        TaxItem(
            tax_code="A",
            tax_rate=0.10,
            tax_amount=0.50,
        )
    )

    receipt.add_item(
        ReceiptItem(
            description="Item",
            total_price=10.00,
        )
    )

    result = receipt.to_dict()

    assert result["store"] == "Sam's Club"
    assert result["subtotal"] == 10.00
    assert result["total"] == 10.50
    assert result["taxes"][0]["tax_code"] == "A"
    assert result["items"][0]["description"] == "Item"
    assert result["validation"] == ["OK"]
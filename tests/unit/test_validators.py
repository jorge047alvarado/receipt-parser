import pytest

from src.models import Receipt, ReceiptItem, TaxItem
from src.validators import ReceiptValidator


@pytest.mark.unit
def test_validate_none_receipt():
    errors = ReceiptValidator.validate(None)

    assert errors == ["Receipt is None."]


@pytest.mark.unit
def test_validate_valid_receipt():
    receipt = Receipt(
        subtotal=5.00,
        tax_total=0.50,
        total=5.50,
        items=[
            ReceiptItem(
                description="Bread",
                total_price=3.00,
            ),
            ReceiptItem(
                description="Milk",
                total_price=2.00,
            ),
        ],
        taxes=[
            TaxItem(
                tax_code="A",
                tax_rate=0.10,
                tax_amount=0.50,
            )
        ],
    )

    errors = ReceiptValidator.validate(receipt)

    assert errors == []


@pytest.mark.unit
def test_validate_subtotal_mismatch():
    receipt = Receipt(
        subtotal=10.00,
        tax_total=0.50,
        total=5.50,
        items=[
            ReceiptItem(
                description="Bread",
                total_price=5.00,
            ),
        ],
        taxes=[
            TaxItem(
                tax_code="A",
                tax_rate=0.10,
                tax_amount=0.50,
            )
        ],
    )

    errors = ReceiptValidator.validate(receipt)

    assert "Subtotal mismatch (OCR=10.00, Calculated=5.00)" in errors


@pytest.mark.unit
def test_validate_tax_mismatch():
    receipt = Receipt(
        subtotal=5.00,
        tax_total=2.00,
        total=7.00,
        items=[
            ReceiptItem(
                description="Bread",
                total_price=5.00,
            ),
        ],
        taxes=[
            TaxItem(
                tax_code="A",
                tax_rate=0.10,
                tax_amount=0.50,
            )
        ],
    )

    errors = ReceiptValidator.validate(receipt)

    assert "Tax mismatch (OCR=2.00, Calculated=0.50)" in errors


@pytest.mark.unit
def test_validate_total_mismatch():
    receipt = Receipt(
        subtotal=5.00,
        tax_total=0.50,
        total=20.00,
        items=[
            ReceiptItem(
                description="Bread",
                total_price=5.00,
            ),
        ],
        taxes=[
            TaxItem(
                tax_code="A",
                tax_rate=0.10,
                tax_amount=0.50,
            )
        ],
    )

    errors = ReceiptValidator.validate(receipt)

    assert "Total mismatch (OCR=20.00, Calculated=5.50)" in errors


@pytest.mark.unit
def test_validate_ignores_tax_items_in_subtotal():
    receipt = Receipt(
        subtotal=5.00,
        tax_total=0.50,
        total=5.50,
        items=[
            ReceiptItem(
                description="Bread",
                total_price=5.00,
            ),
            ReceiptItem(
                description="Tax line",
                total_price=100.00,
                item_type="tax",
            ),
        ],
        taxes=[
            TaxItem(
                tax_code="A",
                tax_rate=0.10,
                tax_amount=0.50,
            )
        ],
    )

    errors = ReceiptValidator.validate(receipt)

    assert errors == []


@pytest.mark.unit
def test_validate_handles_discounts():
    receipt = Receipt(
        subtotal=8.00,
        tax_total=0.00,
        total=8.00,
        items=[
            ReceiptItem(
                description="Item",
                total_price=10.00,
                discount=-2.00,
            )
        ],
        taxes=[],
    )

    errors = ReceiptValidator.validate(receipt)

    assert errors == []


@pytest.mark.unit
def test_validate_multiple_errors():
    receipt = Receipt(
        subtotal=100.00,
        tax_total=20.00,
        total=200.00,
        items=[],
        taxes=[],
    )

    errors = ReceiptValidator.validate(receipt)

    assert len(errors) == 3

@pytest.mark.unit
def test_validate_accepts_values_within_tolerance():
    receipt = Receipt(
        subtotal=5.009,
        tax_total=0.509,
        total=5.509,
        items=[
            ReceiptItem(
                description="Bread",
                total_price=5.00,
            ),
        ],
        taxes=[
            TaxItem(
                tax_code="A",
                tax_rate=0.10,
                tax_amount=0.50,
            )
        ],
    )

    errors = ReceiptValidator.validate(receipt)

    assert errors == []

@pytest.mark.unit
def test_validate_accepts_exact_matching_values():
    receipt = Receipt(
        subtotal=5.00,
        tax_total=0.50,
        total=5.50,
        items=[
            ReceiptItem(
                description="Bread",
                total_price=5.00,
            ),
        ],
        taxes=[
            TaxItem(
                tax_code="A",
                tax_rate=0.10,
                tax_amount=0.50,
            )
        ],
    )

    errors = ReceiptValidator.validate(receipt)

    assert errors == []

@pytest.mark.unit
def test_validate_ignores_missing_ocr_values():
    receipt = Receipt(
        subtotal=None,
        tax_total=None,
        total=None,
        items=[
            ReceiptItem(
                description="Bread",
                total_price=5.00,
            ),
        ],
        taxes=[
            TaxItem(
                tax_code="A",
                tax_rate=0.10,
                tax_amount=0.50,
            )
        ],
    )

    errors = ReceiptValidator.validate(receipt)

    assert errors == []
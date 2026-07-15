import pandas as pd
import pytest

from src.csv_exporter import CSVExporter
from src.models import Receipt, ReceiptItem


@pytest.mark.unit
def test_export_creates_csv_file(tmp_path):
    receipt = Receipt(
        transaction_id="TC 123 456",
        purchase_date="07/11/26",
        purchase_time="14:30",
        store="SAM'S CLUB, PR",
    )

    receipt.add_item(
        ReceiptItem(
            barcode="1234567890",
            description="MILK",
            quantity=2,
            unit_price=3.50,
            total_price=7.00,
            discount=-1.00,
        )
    )

    CSVExporter.OUTPUT_FOLDER = tmp_path

    output_file = CSVExporter.export(receipt)

    assert output_file.exists()
    assert output_file.name == "TC_123_456.csv"


@pytest.mark.unit
def test_export_contains_expected_data(tmp_path):
    receipt = Receipt(
        transaction_id="ABC123",
        purchase_date="07/11/26",
        purchase_time="15:00",
        store="TEST STORE",
    )

    receipt.add_item(
        ReceiptItem(
            barcode="1111111111",
            description="APPLE",
            quantity=3,
            unit_price=1.25,
            total_price=3.75,
            discount=0.00,
            item_type="item",
            tax_code="A",
        )
    )

    CSVExporter.OUTPUT_FOLDER = tmp_path

    output_file = CSVExporter.export(receipt)

    df = pd.read_csv(output_file)

    assert len(df) == 1
    assert df.iloc[0]["Barcode"] == 1111111111
    assert df.iloc[0]["Description"] == "APPLE"
    assert df.iloc[0]["Quantity"] == 3
    assert df.iloc[0]["Final_Price"] == 3.75


@pytest.mark.unit
def test_export_uses_default_filename_when_transaction_missing(tmp_path):
    receipt = Receipt()

    receipt.add_item(
        ReceiptItem(
            description="ITEM",
            total_price=5.00,
        )
    )

    CSVExporter.OUTPUT_FOLDER = tmp_path

    output_file = CSVExporter.export(receipt)

    assert output_file.name == "receipt.csv"


@pytest.mark.unit
def test_export_empty_receipt_creates_empty_csv(tmp_path):
    receipt = Receipt(
        transaction_id="EMPTY"
    )

    CSVExporter.OUTPUT_FOLDER = tmp_path

    output_file = CSVExporter.export(receipt)

    assert output_file.exists()
    assert output_file.read_text().strip() == ""
import json
from pathlib import Path
from dataclasses import asdict

import pytest

from src.ocr import OCRReader
from src.ocr_normalizer import OCRNormalizer
from src.parser import ReceiptParser
from src.models import Receipt


BASE_DIR = Path(__file__).parent

DATA = BASE_DIR / "data"
# EXPECTED = BASE_DIR / "expected"


ocr = OCRReader()
normalizer = OCRNormalizer()
parser = ReceiptParser()


@pytest.mark.integration
@pytest.mark.parametrize(
    "image_file,json_file",
    [
        ("receipt_001.png", "receipt_001_expected.json"),
        ("receipt_002.png", "receipt_002_expected.json"),
    ],
)
def test_receipt(image_file, json_file):

    image_path = DATA / image_file

    #
    # OCR
    #
    lines = ocr.read(image_path)

    #
    # Normalize
    #
    # normalized_lines = normalizer.normalize(raw_lines)

    #
    # Parse
    #
    actual_receipt = parser.parse(lines)

    #
    # Expected Receipt
    #
    with open(DATA / json_file, encoding="utf-8") as f:
        expected_dict = json.load(f)

    expected_receipt = Receipt.from_dict(expected_dict)

    #
    # Compare dataclasses
    #
    assert asdict(actual_receipt) == asdict(expected_receipt)
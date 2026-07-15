import pytest

from src.ocr_normalizer import OCRNormalizer


@pytest.mark.unit
def test_normalize_single_item():
    normalizer = OCRNormalizer()

    lines = [
        "07/11/26 14:30",
        "0980170727",
        "MILK",
        "5.99",
    ]

    result = normalizer.normalize(lines)

    assert result == [
    "07/11/26 14:30",
    "0980170727 MILK 5.99"
    ]


@pytest.mark.unit
def test_normalize_item_with_code():
    normalizer = OCRNormalizer()

    lines = [
        "07/11/26 14:30",
        "0980170727",
        "APPLE",
        "2.99 R",
    ]

    result = normalizer.normalize(lines)

    assert result == ["07/11/26 14:30",
        "0980170727 APPLE 2.99 R"
    ]


@pytest.mark.unit
def test_normalize_multibuy_item():
    normalizer = OCRNormalizer()

    lines = [
        "07/11/26 14:30",
        "0980170727",
        "COFFEE",
        "2 AT",
        "1 FOR 4.97",
        "9.94 R",
    ]

    result = normalizer.normalize(lines)

    assert result == [ "07/11/26 14:30",
        "0980170727 COFFEE",
        "2 AT 1 FOR 4.97 9.94 R"
    ]


@pytest.mark.unit
def test_normalize_subtotal():
    normalizer = OCRNormalizer()

    lines = [
        "SUBTOTAL",
        "25.00",
    ]

    result = normalizer.normalize(lines)

    assert result == [
        "SUBTOTAL 25.00"
    ]


@pytest.mark.unit
def test_normalize_total():
    normalizer = OCRNormalizer()

    lines = [
        "TOTAL",
        "30.00",
    ]

    result = normalizer.normalize(lines)

    assert result == [
        "TOTAL 30.00"
    ]


@pytest.mark.unit
def test_normalize_tax_block():
    normalizer = OCRNormalizer()

    lines = [
        "TAX",
        "1",
        "10.5",
        "2.50",
    ]

    result = normalizer.normalize(lines)

    assert result == [
        "TAX 1 10.5 2.50"
    ]


@pytest.mark.unit
def test_normalize_visa_block():
    normalizer = OCRNormalizer()

    lines = [
        "VISA",
        "****",
        "1234",
    ]

    result = normalizer.normalize(lines)

    assert result == [
        "VISA **** 1234"
    ]


@pytest.mark.unit
def test_normalize_inst_sv():
    normalizer = OCRNormalizer()

    lines = [
        "INST SV",
        "COCOA PEBBL",
        "3.00-T",
    ]

    result = normalizer.normalize(lines)

    assert result == [
        "INST SV COCOA PEBBL",
        "3.00-T"
    ]


@pytest.mark.unit
def test_normalize_default_lines():
    normalizer = OCRNormalizer()

    lines = [
        "RANDOM TEXT"
    ]

    result = normalizer.normalize(lines)

    assert result == [
        "RANDOM TEXT"
    ]

@pytest.mark.unit
def test_normalize_barcode_without_price():
    normalizer = OCRNormalizer()

    lines = [
        "07/11/26 14:30",
        "0980170727",
        "UNKNOWN ITEM",
    ]

    result = normalizer.normalize(lines)

    assert result == [
        "07/11/26 14:30",
        "0980170727 UNKNOWN ITEM",
    ]

@pytest.mark.unit
def test_normalize_inst_sv_multibuy():
    normalizer = OCRNormalizer()

    lines = [
        "INST SV",
        "COFFEE",
        "2 AT",
        "1 FOR 4.97",
        "9.94 R",
    ]

    result = normalizer.normalize(lines)

    assert result == [
        "INST SV COFFEE",
        "2 AT 1 FOR 4.97 9.94 R",
    ]

@pytest.mark.unit
def test_normalize_inst_sv_discount_line():
    normalizer = OCRNormalizer()

    lines = [
        "INST SV",
        "DEGREE MEN",
        "3.00-T",
    ]

    result = normalizer.normalize(lines)

    assert result == [
        "INST SV DEGREE MEN",
        "3.00-T",
    ]

@pytest.mark.unit
def test_normalize_tax_multiple_lines():
    normalizer = OCRNormalizer()

    lines = [
        "TAX",
        "1",
        "6%",
        "0.30",
    ]

    result = normalizer.normalize(lines)

    assert result == [
        "TAX 1 6% 0.30"
    ]

@pytest.mark.unit
def test_normalize_visa_block_with_multiple_parts():
    normalizer = OCRNormalizer()

    lines = [
        "VISA",
        "CREDIT",
        "1234",
    ]

    result = normalizer.normalize(lines)

    assert result == [
        "VISA CREDIT 1234"
    ]

@pytest.mark.unit
def test_normalize_barcode_without_price_or_following_data():
    normalizer = OCRNormalizer()

    lines = [
        "07/11/26 14:30",
        "0980170727",
        "UNKNOWN ITEM",
        "NEXT LINE",
    ]

    result = normalizer.normalize(lines)

    assert result == [
        "07/11/26 14:30",
        "0980170727 UNKNOWN ITEM NEXT LINE"
        ]

@pytest.mark.unit
def test_normalize_inst_sv_with_multibuy_discount():
    normalizer = OCRNormalizer()

    lines = [
        "INST SV",
        "COFFEE",
        "2 AT",
        "1 FOR 4.97",
        "9.94 R",
    ]

    result = normalizer.normalize(lines)

    assert result == [
        "INST SV COFFEE",
        "2 AT 1 FOR 4.97 9.94 R",
    ]

@pytest.mark.unit
def test_normalize_inst_sv_regular_discount():
    normalizer = OCRNormalizer()

    lines = [
        "INST SV",
        "DEGREE MEN",
        "3.00-T",
        "NEXT",
    ]

    result = normalizer.normalize(lines)

    assert result == [
        "INST SV DEGREE MEN",
        "3.00-T",
        "NEXT",
    ]

@pytest.mark.unit
def test_normalize_tax_without_final_amount():
    normalizer = OCRNormalizer()

    lines = [
        "TAX",
        "1",
        "6%",
    ]

    result = normalizer.normalize(lines)

    assert result == [
        "TAX 1 6%"
    ]

@pytest.mark.unit
def test_normalize_visa_without_last_four_digits():
    normalizer = OCRNormalizer()

    lines = [
        "VISA",
        "CREDIT",
    ]

    result = normalizer.normalize(lines)

    assert result == [
        "VISA CREDIT"
    ]

@pytest.mark.unit
def test_normalize_barcode_without_price_or_multibuy():
    normalizer = OCRNormalizer()

    lines = [
        "07/11/26 14:30",
        "0980170727",
        "UNKNOWN ITEM",
        "NOT A PRICE",
    ]

    result = normalizer.normalize(lines)

    print(result)

    assert result == [
        "07/11/26 14:30",
        "0980170727 UNKNOWN ITEM NOT A PRICE"]

@pytest.mark.unit
def test_normalize_tax_empty_after_header():
    normalizer = OCRNormalizer()

    lines = [
        "TAX",
    ]

    result = normalizer.normalize(lines)

    assert result == [
        "TAX"
    ]
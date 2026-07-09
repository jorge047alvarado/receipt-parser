from pathlib import Path
import json

from src.ocr import OCRReader
from src.parser import ReceiptParser
from src.validators import ReceiptValidator
from src.csv_exporter import CSVExporter


INPUT_FOLDER = Path("input")
OUTPUT_FOLDER = Path("output")


def process_receipt(image_path: Path):
    """
    Process a single receipt image.
    """

    print(f"\nProcessing: {image_path.name}")

    #
    # OCR
    #

    ocr = OCRReader()

    lines = ocr.read(image_path)

    #
    # Debug OCR output
    #

    print("\n----- OCR LINES -----")

    for idx, line in enumerate(lines):
        print(f"{idx:03}: {line}")

    #
    # Parse
    #

    parser = ReceiptParser(lines)

    receipt = parser.parse()

    #
    # Validate
    #

    receipt.validation = ReceiptValidator.validate(receipt)

    #
    # Save JSON
    #

    OUTPUT_FOLDER.mkdir(exist_ok=True)

    json_path = OUTPUT_FOLDER / f"{image_path.stem}.json"

    with open(json_path, "w", encoding="utf-8") as f:

        json.dump(
            receipt.to_dict(),
            f,
            indent=4,
            ensure_ascii=False,
        )

    #
    # Save CSV
    #

    csv_path = CSVExporter.export(receipt)

    #
    # Summary
    #

    print("\nITEM BREAKDOWN")

    for item in receipt.items:

        print(
            item.description,
            item.quantity,
            item.unit_price,
            item.total_price,
            item.discount,
            item.tax_code,
        )

    print("\nRECEIPT TOTALS")
    print("----------------")

    print(f"Subtotal : {receipt.subtotal:.2f}")
    print(f"Tax      : {receipt.tax:.2f}")
    print(f"Total    : {receipt.total:.2f}")

    if receipt.validation:

        print("\nValidation Errors:")

        for error in receipt.validation:

            print(f" - {error}")

    else:

        print("\nValidation: PASSED")

    print(f"\nJSON saved to: {json_path}")
    print(f"CSV saved to : {csv_path}")


def main():

    if not INPUT_FOLDER.exists():

        print("Input folder not found.")

        return

    images = []

    for ext in ("*.jpg", "*.jpeg", "*.png", "*.bmp", "*.tif", "*.tiff"):

        images.extend(INPUT_FOLDER.glob(ext))

    if not images:

        print("No receipt images found.")

        return

    for image in sorted(images):

        process_receipt(image)


if __name__ == "__main__":

    main()
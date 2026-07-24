from pathlib import Path
import pandas as pd

from src.models import Receipt


class CSVExporter:
    """
    Export a parsed receipt to CSV.
    """

    OUTPUT_FOLDER = Path("output")

    @classmethod
    def export(cls, receipt: Receipt) -> Path:
        """
        Export a receipt to a CSV file.

        Returns
        -------
        Path
            Path of the generated CSV.
        """

        cls.OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

        rows = []

        for item in receipt.items:

            print(item.item_type)

            rows.append(
                {
                    "Purchase_Date": receipt.purchase_date,
                    "Total_Price": item.total_price,
                    "Unit_Price": item.unit_price,
                    "Quantity": item.quantity,
                    "Store": receipt.store,
                    "Description": item.description,
                    "Barcode": item.barcode,
                    "Discount": item.discount,
                    "Final_Price": item.final_price,
                    "Item_code": item.item_code,
                    "Transaction_ID": receipt.transaction_id,
                    "Item_Type": item.item_type,
                }
            )

        df = pd.DataFrame(rows)

        filename = (
            receipt.transaction_id.replace(" ", "_")
            if receipt.transaction_id
            else "receipt"
        )

        output_file = cls.OUTPUT_FOLDER / f"{filename}.csv"

        df.to_csv(output_file, index=False)

        return output_file
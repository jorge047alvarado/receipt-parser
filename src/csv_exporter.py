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

            rows.append(
                {
                    "Transaction_ID": receipt.transaction_id,
                    "Purchase_Date": receipt.purchase_date,
                    "Purchase_Time": receipt.purchase_time,
                    "Store": receipt.store,
                    "Barcode": item.barcode,
                    "Description": item.description,
                    "Quantity": item.quantity,
                    "Unit_Price": item.unit_price,
                    "Total_Price": item.total_price,
                    "Discount": item.discount,
                    "Final_Price": item.final_price,
                    "Item_Type": item.item_type,
                    "Item_code": item.item_code,
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
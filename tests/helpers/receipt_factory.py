from src.models import Receipt, ReceiptItem, TaxItem


def receipt_from_dict(data: dict) -> Receipt:
    receipt = Receipt()

    receipt.store = data["store"]
    receipt.purchase_date = data["purchase_date"]
    receipt.purchase_time = data["purchase_time"]
    receipt.transaction_id = data["transaction_id"]
    receipt.subtotal = data["subtotal"]
    receipt.total = data["total"]
    receipt.cash_rewards = data["cash_rewards"]
    receipt.tax_total = data["tax"]

    for tax in data["taxes"]:
        receipt.add_tax(
            TaxItem(
                tax_code=tax["tax_code"],
                tax_rate=tax["tax_rate"],
                tax_amount=tax["tax_amount"],
            )
        )

    for item in data["items"]:
        receipt.add_item(
            ReceiptItem(
                barcode=item["barcode"],
                description=item["description"],
                quantity=item["quantity"],
                unit_price=item["unit_price"],
                total_price=item["total_price"],
                discount=item["discount"],
                item_code=item["item_code"],
                item_type=item["item_type"],
                tax_code=item["tax_code"],
            )
        )

    return receipt
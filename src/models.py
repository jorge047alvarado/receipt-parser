from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


# ----------------------------------------------------------------------
# Receipt Item
# ----------------------------------------------------------------------
@dataclass
class ReceiptItem:
    barcode: Optional[str] = None
    description: str = ""

    quantity: int = 1
    unit_price: float = 0.0
    total_price: float = 0.0

    discount: float = 0.0

    pack_size: Optional[str] = None
    item_code: Optional[str] = None

    # Future use if you decide to classify items
    tax_code: Optional[str] = None


# ----------------------------------------------------------------------
# Tax Line
# ----------------------------------------------------------------------
@dataclass
class TaxItem:
    tax_code: str
    tax_rate: float
    tax_amount: float


# ----------------------------------------------------------------------
# Receipt
# ----------------------------------------------------------------------
@dataclass
class Receipt:
    purchase_date: Optional[str] = None
    receipt_id: Optional[str] = None

    store: str = ""

    subtotal: float = 0.0
    total_tax: float = 0.0
    total: float = 0.0

    items: list[ReceiptItem] = field(default_factory=list)
    taxes: list[TaxItem] = field(default_factory=list)

    validation_errors: list[str] = field(default_factory=list)

    def add_item(self, item: ReceiptItem):
        self.items.append(item)

    def add_tax(self, tax: TaxItem):
        self.taxes.append(tax)

    @property
    def calculated_subtotal(self) -> float:
        return round(
            sum(item.total_price + item.discount for item in self.items),
            2,
        )

    @property
    def calculated_tax(self) -> float:
        return round(
            sum(tax.tax_amount for tax in self.taxes),
            2,
        )

    @property
    def calculated_total(self) -> float:
        return round(
            self.calculated_subtotal + self.calculated_tax,
            2,
        )
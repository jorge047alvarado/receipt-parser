from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Optional, Any, Dict

# ----------------------------------------------------------------------
# Tax Item
# ----------------------------------------------------------------------
@dataclass
class TaxItem:
    tax_code: str
    tax_rate: float
    tax_amount: float

# ----------------------------------------------------------------------
# Receipt Item
# ----------------------------------------------------------------------
@dataclass
class ReceiptItem:
    """
    Represents either a merchandise item or a tax line.
    """

    barcode: Optional[str] = None
    description: str = ""

    quantity: int = 1
    unit_price: float = 0.0
    total_price: float = 0.0

    discount: float = 0.0

    # Sam's Club item code (Y, T, R, P, etc.)
    item_code: Optional[str] = None

    # "item" or "tax"
    item_type: str = "item"

    # Tax group number for tax lines
    tax_code: Optional[str] = None

    @property
    def final_price(self) -> float:
        """
        Actual amount paid after discounts.
        """
        return round(self.total_price + self.discount, 2)

    @property
    def is_tax(self) -> bool:
        return self.item_type == "tax"

    @property
    def is_merchandise(self) -> bool:
        return self.item_type == "item"

    @property
    def is_discounted(self) -> bool:
        return self.discount != 0

    def to_dict(self) -> dict:
        return asdict(self) | {
            "final_price": self.final_price
        }
    
    @classmethod
    def from_dict(cls, dictionary: Dict[str, Any]) -> "ReceiptItem":

        return cls(
            barcode=dictionary["barcode"],
            description=dictionary["description"],
            quantity=dictionary["quantity"],
            unit_price=dictionary["unit_price"],
            total_price=dictionary["total_price"],
            discount=dictionary["discount"],
            item_code=dictionary["item_code"],
            item_type=dictionary["item_type"],
            tax_code=dictionary["tax_code"]
        )


# ----------------------------------------------------------------------
# Receipt
# ----------------------------------------------------------------------
@dataclass
class Receipt:
    purchase_date: Optional[str] = None
    purchase_time: Optional[str] = None
    transaction_id: Optional[str] = None

    store: str = ""

    subtotal: float = 0.0
    tax: float = 0.0
    tax_total: float = 0.0
    total: float = 0.0
    taxes: list[TaxItem] = field(default_factory=list)
    cash_rewards: float = 0.0

    items: list[ReceiptItem] = field(default_factory=list)

    validation: list[str] = field(default_factory=list)

    def add_item(self, item: ReceiptItem):
        self.items.append(item)
    
    def add_tax(self, tax: TaxItem):
        self.taxes.append(tax)

    @property
    def merchandise_items(self) -> list[ReceiptItem]:
        return [
            item
            for item in self.items
            if item.is_merchandise
        ]

    @property
    def tax_items(self) -> list[ReceiptItem]:
        return [
            item
            for item in self.items
            if item.is_tax
        ]

    @property
    def total_discount(self) -> float:
        return round(
            sum(item.discount for item in self.merchandise_items),
            2,
        )

    @property
    def calculated_subtotal(self) -> float:
        """
        Shelf subtotal before taxes.
        Discounts reduce the subtotal.
        """
        return round(
            sum(item.final_price for item in self.merchandise_items),
            2,
        )

    @property
    def calculated_tax(self) -> float:
        return round(
            sum(t.tax_amount for t in self.taxes),
            2,
        )

    @property
    def calculated_total(self) -> float:
        return round(
            self.calculated_subtotal +
            self.calculated_tax,
            2,
        )
    
    def to_dict(self) -> dict:
        return {
            "purchase_date": self.purchase_date,
            "purchase_time": self.purchase_time,
            "transaction_id": self.transaction_id,
            "cash_rewards": self.cash_rewards,
            "store": self.store,
            "subtotal": self.subtotal,
            "tax": self.tax,
            "taxes": [{"tax_code": t.tax_code,
                       "tax_rate": t.tax_rate,
                       "tax_amount": t.tax_amount}
                           for t in self.taxes],
            "total": self.total,
            "items": [
                item.to_dict()
                for item in self.items
            ],
            "validation": self.validation,
        }
    
    @classmethod
    def from_dict(cls, dictionary: Dict[str, Any]) -> Receipt:

        return cls(
            purchase_date=dictionary['purchase_date'],
            purchase_time=dictionary['purchase_time'],
            transaction_id=dictionary['transaction_id'],
            cash_rewards=dictionary['cash_rewards'],
            store=dictionary['store'],
            subtotal=dictionary['subtotal'],
            tax=dictionary['tax'],
            tax_total=dictionary['tax'],
            taxes=[{"tax_code":tax['tax_code'], "tax_rate": tax['tax_rate'], "tax_amount": tax['tax_amount']} for tax in dictionary['taxes']],
            total=dictionary['total'],
            items=[ReceiptItem.from_dict(item) for item in dictionary.get("items", [])],
            validation= dictionary['validation'],
        )
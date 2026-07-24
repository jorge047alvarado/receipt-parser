from __future__ import annotations

from typing import Optional

from src.models import Receipt, ReceiptItem , TaxItem
from src import patterns


class ReceiptParser:
    """
    Parses OCR lines into a Receipt object.
    """

    def __init__(self):
        self.receipt: Optional[Receipt] = None
        self.pending_item: Optional[ReceiptItem] = None
        self.pending_discount_item: Optional[ReceiptItem] = None   

        #
        # Ordered list of parsing handlers.
        #
        self.handlers = [
            self._parse_store,
            self._parse_header,
            self._parse_tax,
            self._parse_totals,
            self._parse_discount,
            self._parse_item,
            self._cash_rewards,
        ] 

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def parse(self, lines: list[str]) -> Receipt:
        """
        Parse OCR text lines into a Receipt.
        """

        self.receipt = Receipt()
        self.pending_item = None
        self.pending_discount_item = None

        for raw_line in lines:

            line = raw_line.strip()

            if not line:
                continue

            #
            # Before parsing discounts, flush any pending item.
            # #
            if line.upper().startswith("INST SV"):
                self._finalize_pending_item()
            
            handled = False

            for handler in self.handlers:

                if handler(line):
                    handled = True
                    break

            if handled:
                continue

        self._finalize_pending_item()

        #
        # Compute OCR tax total from all parsed tax lines.
        #
        self.receipt.tax_total = round(
            sum(tax.tax_amount for tax in self.receipt.taxes),
            2,
        )

        self.receipt.tax = self.receipt.tax_total

        return self.receipt

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _start_new_item(self, item: ReceiptItem):
        """
        Flush any existing pending item before beginning a new one.
        """

        self._finalize_pending_item()
        self.pending_item = item

    def _finalize_pending_item(self):
        """
        Store the current pending item in the receipt.
        """

        if self.pending_item is None:
            return

        self.receipt.add_item(self.pending_item)
        self.pending_item = None

    def _current_item(self) -> Optional[ReceiptItem]:
        return self.pending_item

    # ------------------------------------------------------------------
    # Placeholder methods
    # These will be implemented in later steps.
    # ------------------------------------------------------------------



    def _parse_item(self, line: str) -> bool:
        """
        Parse merchandise items.

        Supports:
            • Regular items
            • Multibuy continuation lines
        """

        #
        # ----------------------------------------------------------
        # NORMAL ITEM
        #
        # Example:
        #
        # 0980170727 MMBROCCHEDS 10.98 Y
        #
        # ----------------------------------------------------------
        #

        match = patterns.ITEM_RE.match(line)

        if match:

            price = float(match.group("price"))

            item = ReceiptItem(
                barcode=match.group("barcode"),
                description=match.group("description").strip(),
                quantity=1,
                unit_price=price,
                total_price=price,
                item_code=match.group("item_code"),
            )

            self.receipt.add_item(item)

            return True
        
        match = patterns.MULTIBUY_HEADER_RE.match(line)

        if match:

            item = ReceiptItem(
                barcode=match.group("barcode"),
                description=match.group("description").strip(),
            )

            self._start_new_item(item)

            return True

        #
        # ----------------------------------------------------------
        # MULTIBUY
        #
        # Example:
        #
        # 2 AT 1 FOR 4.97 9.94 R
        #
        # ----------------------------------------------------------
        #

        match = patterns.MULTIBUY_RE.match(line)

        if match and self.pending_item:

            self.pending_item.quantity = int(match.group("quantity"))

            self.pending_item.unit_price = float(
                match.group("unit_price")
            )

            self.pending_item.total_price = float(
                match.group("total_price")
            )

            self.pending_item.item_code = match.group("item_code")

            self._finalize_pending_item()

            return True
        
    def _parse_discount(self, line: str) -> bool:

        """
        Parse Instant Savings (INST SV) discount lines.

        Supports:

            INST SV COCOA PEBBL 1.25-¥

        and

            INST SV MDAIRFRYER
            2 AT 1 FOR 6.00- 12.00-T
        """

        #
        # ----------------------------------------------------------
        # Second line of a multibuy discount
        # ----------------------------------------------------------
        #

        if self.pending_discount_item:

            match= patterns.MULTIBUY_DISCOUNT_RE.match(line)

            if match:

                self.pending_discount_item.discount = -float(
                    match.group("discount")
                )

                self.pending_discount_item = None

                return True
            
            match = patterns.DISCOUNT_INCOMPLETE_RE.match(line)

            if match:

                self.pending_discount_item.discount = -float(
                    match.group("discount")
                )

                self.pending_discount_item = None

                return True

        #
        # ----------------------------------------------------------
        # Single-line discount
        # ----------------------------------------------------------
        #

        match = patterns.DISCOUNT_RE.match(line)

        if match:

            description = " ".join(
                match.group("description").strip().upper().split()
            )

            discount = -float(match.group("discount"))

            #
            # Find the most recent matching item.
            #

            for item in reversed(self.receipt.items):

                item_description = " ".join(
                    item.description.strip().upper().split()
                )

                if item_description == description:

                    item.discount = discount

                    return True

            return False

        #
        # ----------------------------------------------------------
        # First line of a multibuy discount
        # ----------------------------------------------------------
        #

        match = patterns.DISCOUNT_HEADER_RE.match(line)    

        if match:

            description = " ".join(
                match.group("description").strip().upper().split()
            )

            for item in reversed(self.receipt.items):

                item_description = " ".join(
                    item.description.strip().upper().split()
                )

                if item_description == description:

                    self.pending_discount_item = item

                    return True
            
            item = ReceiptItem(
                barcode=0,
                description=line,
                quantity=0,
                unit_price=0,
                total_price=0,
                item_code='Z',
                item_type='MISSED-ITEM-AND-DISCOUNT',
            )

            self.receipt.add_item(item)      

        return False

    def _parse_tax(self, line: str) -> bool:
        """
        Parse tax lines.

        Supports:

            TAX 1 10.5 % 21.09
            TAX 2 1 % 4.48
            TAX 4 6 % 0.30

        and

            10.5% TAX 1 21.09
            1% TAX 2 4.48
            6% TAX 4 0.30
        """

        match = patterns.TAX_RE.match(line)

        if not match:
            return False

        # rate = float(match.group("rate1") or match.group("rate2"))
        rate = float(match.group("rate"))

        # tax_code = match.group("code1") or match.group("code2")
        tax_code = match.group("code")

        amount = float(match.group("amount"))

        self.receipt.add_tax(
            TaxItem(
                tax_code=tax_code,
                tax_rate=rate,
                tax_amount=amount,
            )
        )

        item = ReceiptItem(
                barcode=0,
                description=("TAX " + str(tax_code) + " " + str(rate) + "%"),
                quantity=0,
                unit_price=amount,
                total_price=amount,
                item_type='tax',
            )

        self.receipt.add_item(item) 

        return True

    def _parse_totals(self, line: str) -> bool:
        """
        Parse receipt totals.
        """

        #
        # Subtotal
        #

        match = patterns.SUBTOTAL_RE.match(line)

        if match:

            self.receipt.subtotal = float(match.group("subtotal"))

            return True

        #
        # Total
        #

        match = patterns.TOTAL_RE.match(line)

        if match:

            self.receipt.total = float(match.group("total"))

            return True

        return False

    def _parse_header(self, line: str) -> bool:
        """
        Parse receipt header information.

        Handles:
            - Purchase date/time
            - Transaction ID (TCH ...)
        """

        #
        # Purchase date/time
        #

        match = patterns.DATE_TIME_RE.match(line)

        if match:

            self.receipt.purchase_date = match.group("date")
            self.receipt.purchase_time = match.group("time")

            return True

        #
        # Transaction ID
        #
        match = patterns.TRANSACTION_ID_RE.match(line.strip())

        if match:

            self.receipt.transaction_id = line.strip()

            return True

        return False
    
    def _cash_rewards(self, line: str) -> bool:
        """
        Parse cash rewards line.

        Example:
            CASH REWARDS 1.00
        """

        match = patterns.CASH_REWARDS_RE.match(line)

        if match:

            self.receipt.cash_rewards = -float(match.group("amount"))

            self.receipt.add_item(
                ReceiptItem(
                    description=match.group("description"),
                    quantity=1,
                    unit_price=-float(match.group("amount")),
                    total_price=float(match.group("amount")),
                    discount=0.0,
                    item_type="cash_rewards",
                )
            )

            return True

        return False

    def _parse_store(self, line: str) -> bool:

        upper = line.upper().strip()

        if upper.startswith("SAM'S CLUB"):
            self.receipt.store = upper
            return True

        if upper.startswith("MAYAGUEZ, PR"):
            self.receipt.store += " " + upper
            return True

        return False
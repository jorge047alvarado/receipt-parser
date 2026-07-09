from src.models import Receipt


class ReceiptValidator:
    """
    Validates a parsed receipt against the OCR totals.

    The validator never modifies the receipt.
    It only reports inconsistencies.
    """

    TOLERANCE = 0.01

    @staticmethod
    def validate(receipt: Receipt) -> list[str]:
        """
        Validate the parsed receipt.

        Returns:
            List of validation errors.
        """

        if receipt is None:
            return ["Receipt is None."]

        errors = []

        calculated_subtotal = ReceiptValidator._calculate_subtotal(receipt)
        calculated_tax = ReceiptValidator._calculate_tax(receipt)
        calculated_total = round(calculated_subtotal + calculated_tax, 2)

        #
        # Subtotal
        #

        if receipt.subtotal is not None:

            if abs(receipt.subtotal - calculated_subtotal) > ReceiptValidator.TOLERANCE:

                errors.append(
                    f"Subtotal mismatch (OCR={receipt.subtotal:.2f}, Calculated={calculated_subtotal:.2f})"
                )

        #
        # Tax
        #

        if receipt.tax is not None:

            if abs(receipt.tax - calculated_tax) > ReceiptValidator.TOLERANCE:

                errors.append(
                    f"Tax mismatch (OCR={receipt.tax:.2f}, Calculated={calculated_tax:.2f})"
                )

        #
        # Total
        #

        if receipt.total is not None:

            if abs(receipt.total - calculated_total) > ReceiptValidator.TOLERANCE:

                errors.append(
                    f"Total mismatch (OCR={receipt.total:.2f}, Calculated={calculated_total:.2f})"
                )

        return errors

    @staticmethod
    def _calculate_subtotal(receipt: Receipt) -> float:
        """
        Merchandise subtotal before taxes.

        Discounts are stored as negative numbers, so
        total_price - discount restores the shelf price.
        """

        subtotal = 0.0

        for item in receipt.items:

            if item.item_type != "item":
                continue

            subtotal += item.total_price

        return round(subtotal, 2)

    @staticmethod
    def _calculate_tax(receipt: Receipt) -> float:
        """
        Sum every parsed tax line.
        """

        tax = 0.0

        for item in receipt.items:

            if item.item_type != "tax":
                continue

            tax += item.total_price

        return round(tax, 2)
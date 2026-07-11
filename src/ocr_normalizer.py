from __future__ import annotations

import re

class OCRNormalizer:
    """
    Converts PaddleOCR fragmented output into the line format expected
    by ReceiptParser.
    """

    # BARCODE_RE = re.compile(r"^\d{10}$")

    BARCODE_RE = re.compile(r"^\d{10,11}\b")

    DATE_TIME_RE = re.compile(
    r"""
    ^
    \d{2}/\d{2}/\d{2}
    \s+
    \d{2}:\d{2}
    (?:\s+.*)?      # allow terminal/register info
    $
    """,
    re.VERBOSE,
    )

    STORE_CITY_RE = re.compile(
        r"^[A-Z ]+,\s*[A-Z]{2}$",
        re.IGNORECASE,
    )

    PRICE_RE = re.compile(
        r"^\d+\.\d{2}(?:-)?\s*[A-Z]$"
    )

    MULTIBUY_START_RE = re.compile(
        r"^\d+\s+AT$"
    )

    HEADER_VALUE_RE = {
        "SUBTOTAL",
        "TOTAL",
        "CASH REWARDS TEND",
        "VISA CREDIT TEND",
        "CHANGE DUE",
        "SHOPPING CARD REDEMPTION",
    }

    def normalize(self, lines: list[str]) -> list[str]:

        result = []

        i = 0

        header_finished = False

        while i < len(lines):

            line = lines[i].strip()

            if self.DATE_TIME_RE.match(line):
                header_finished = True

            #
            # ------------------------------------------------------
            # BARCODE
            # ------------------------------------------------------
            #

            if header_finished and self.BARCODE_RE.match(line):

                barcode = line

                i += 1

                description_parts = []

                #
                # Read description until we reach either:
                #
                #  - price line
                #  - multibuy
                #
                while i < len(lines):

                    current = lines[i].strip()

                    if self.PRICE_RE.match(current):
                        break

                    if self.MULTIBUY_START_RE.match(current):
                        break

                    description_parts.append(current)
                    i += 1

                description = " ".join(description_parts).strip()

                #
                # Single price item
                #

                if i < len(lines):

                    current = lines[i].strip()

                    if self.PRICE_RE.match(current):

                        result.append(
                            f"{barcode} {description} {current}"
                        )

                        i += 1
                        continue

                #
                # Multibuy
                #

                if (
                    i < len(lines)
                    and self.MULTIBUY_START_RE.match(lines[i].strip())
                ):

                    mb = [lines[i].strip()]

                    i += 1

                    #
                    # Consume until we reach the final price line.
                    #

                    while i < len(lines):

                        part = lines[i].strip()

                        mb.append(part)

                        if self.PRICE_RE.match(part):
                            break

                        i += 1

                    result.append(
                        f"{barcode} {description}"
                    )

                    result.append(
                        " ".join(mb)
                    )

                    i += 1
                    continue

                result.append(
                    f"{barcode} {description}"
                ) # The code seems to never reach this point, but it's here for completeness.

                continue

            #
            # ------------------------------------------------------
            # INST SV
            # ------------------------------------------------------
            #

            if line == "INST SV":

                description = ""

                if i + 1 < len(lines):

                    description = lines[i + 1].strip()

                result.append(
                    f"INST SV {description}"
                )

                i += 2

                #
                # Merge multibuy discount
                #

                if (
                    i < len(lines)
                    and self.MULTIBUY_START_RE.match(lines[i])
                ):

                    mb = [lines[i].strip()]

                    i += 1

                    while i < len(lines):

                        part = lines[i].strip()

                        mb.append(part)

                        if self.PRICE_RE.match(part):
                            break

                        i += 1

                    result.append(
                        " ".join(mb)
                    )

                    i += 1

                elif i < len(lines):

                    result.append(lines[i].strip())
                    i += 1

                continue

            #
            # ------------------------------------------------------
            # SUBTOTAL / TOTAL / PAYMENTS
            # ------------------------------------------------------
            #

            if line in self.HEADER_VALUE_RE:

                if i + 1 < len(lines):

                    result.append(
                        f"{line} {lines[i+1].strip()}"
                    )

                    i += 2
                    continue

            #
            # ------------------------------------------------------
            # TAX
            # ------------------------------------------------------
            #

            if line == "TAX":

                pieces = ["TAX"]

                i += 1

                while i < len(lines):

                    pieces.append(lines[i].strip())

                    if re.match(r"^\d+\.\d{2}$", lines[i].strip()):
                        break

                    i += 1

                result.append(" ".join(pieces))

                i += 1
                continue

            #
            # ------------------------------------------------------
            # VISA MASK
            # ------------------------------------------------------
            #

            if line == "VISA":

                pieces = ["VISA"]

                i += 1

                while i < len(lines):

                    part = lines[i].strip()

                    pieces.append(part)

                    if re.fullmatch(r"\d{4}", part):
                        break

                    i += 1

                result.append(" ".join(pieces))

                i += 1
                continue

            #
            # Default
            #

            result.append(line)

            i += 1

        return result
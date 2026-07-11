from pathlib import Path
from paddleocr import PaddleOCR
from src.ocr_normalizer import OCRNormalizer


class OCRReader:
    """
    Wrapper around PaddleOCR.

    This class is responsible only for extracting text from
    receipt images. It knows nothing about receipt parsing.
    """

    def __init__(self, use_gpu: bool = True):

        self.ocr = PaddleOCR(
            lang="en",
            use_doc_orientation_classify=False,
            use_doc_unwarping=False,
            use_textline_orientation=False,
            device="gpu:0" if use_gpu else "cpu",
        )

    def read(self, image_path: str | Path) -> list[str]:
        """
        Read a receipt image and return the OCR lines.

        Parameters
        ----------
        image_path
            Path to the receipt image.

        Returns
        -------
        list[str]
            OCR text lines in reading order.
        """

        result = self.ocr.predict(str(image_path))

        lines = []

        #
        # PaddleOCR returns one PageResult per page.
        #

        for page in result:

            #
            # Each detected text line.
            #

            rec_texts = page.get("rec_texts", [])

            for text in rec_texts:

                text = text.strip()

                if text:

                    lines.append(text)

        normalizer = OCRNormalizer()
        
        return normalizer.normalize(lines)
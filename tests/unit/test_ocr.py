import pytest

from src.ocr import OCRReader


@pytest.mark.unit
def test_ocr_reader_initializes_with_cpu(mocker):
    paddle_mock = mocker.patch(
        "src.ocr.PaddleOCR"
    )

    OCRReader(use_gpu=False)

    paddle_mock.assert_called_once_with(
        lang="en",
        use_doc_orientation_classify=False,
        use_doc_unwarping=False,
        use_textline_orientation=False,
        device="cpu",
    )


@pytest.mark.unit
def test_ocr_reader_initializes_with_gpu(mocker):
    paddle_mock = mocker.patch(
        "src.ocr.PaddleOCR"
    )

    OCRReader(use_gpu=True)

    paddle_mock.assert_called_once_with(
        lang="en",
        use_doc_orientation_classify=False,
        use_doc_unwarping=False,
        use_textline_orientation=False,
        device="gpu:0",
    )


@pytest.mark.unit
def test_ocr_reader_reads_and_normalizes_lines(mocker):
    paddle_instance = mocker.Mock()

    paddle_instance.predict.return_value = [
        {
            "rec_texts": [
                "  ITEM ONE  ",
                "",
                "ITEM TWO",
                "   ",
            ]
        }
    ]

    mocker.patch(
        "src.ocr.PaddleOCR",
        return_value=paddle_instance,
    )

    normalizer = mocker.patch(
        "src.ocr.OCRNormalizer"
    )

    normalizer.return_value.normalize.return_value = [
        "ITEM ONE",
        "ITEM TWO",
    ]

    reader = OCRReader(use_gpu=False)

    result = reader.read("receipt.jpg")

    paddle_instance.predict.assert_called_once_with(
        "receipt.jpg"
    )

    normalizer.return_value.normalize.assert_called_once_with(
        [
            "ITEM ONE",
            "ITEM TWO",
        ]
    )

    assert result == [
        "ITEM ONE",
        "ITEM TWO",
    ]


@pytest.mark.unit
def test_ocr_reader_handles_missing_rec_texts(mocker):
    paddle_instance = mocker.Mock()

    paddle_instance.predict.return_value = [
        {},
        {
            "rec_texts": [
                "TEXT"
            ]
        }
    ]

    mocker.patch(
        "src.ocr.PaddleOCR",
        return_value=paddle_instance,
    )

    normalizer = mocker.patch(
        "src.ocr.OCRNormalizer"
    )

    normalizer.return_value.normalize.return_value = [
        "TEXT"
    ]

    reader = OCRReader(use_gpu=False)

    result = reader.read("receipt.jpg")

    assert result == ["TEXT"]
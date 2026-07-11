import pytest

@pytest.fixture
def sample_receipt_text():
    return """
    Walmart

    Bread      3.50
    Milk       4.00

    Tax        0.60

    Total      8.10
    """
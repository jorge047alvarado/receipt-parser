def assert_receipts_equal(actual, expected):

    assert actual.store == expected.store
    assert actual.purchase_date == expected.purchase_date
    assert actual.purchase_time == expected.purchase_time
    assert actual.transaction_id == expected.transaction_id

    assert actual.subtotal == expected.subtotal
    assert actual.total == expected.total
    assert actual.cash_rewards == expected.cash_rewards
    assert actual.tax_total == expected.tax_total

    assert len(actual.taxes) == len(expected.taxes)
    assert len(actual.items) == len(expected.items)

    for actual_tax, expected_tax in zip(actual.taxes, expected.taxes):
        assert actual_tax == expected_tax

    for actual_item, expected_item in zip(actual.items, expected.items):
        assert actual_item == expected_item
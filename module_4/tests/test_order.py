"""
Module: test_order.py
Author: Billy Presume
Created: 2025-06-17
Modified: 2025-06-17
Description: Contains unit tests for the Order class. Verifies order
initialization, pizza addition, cost updates, and order payment status.
"""

import pytest
from src.order import Order

pytestmark = pytest.mark.order


def test_order_init():
    """
    Test initialization of an Order object.

    Asserts:
        - Pizza list is empty.
        - Total cost is zero.
        - Payment status is unpaid.
    """
    order = Order()
    assert order.pizzas == []
    assert order.total_cost == 0
    assert not order.paid


def test_order_input_pizza():
    """
    Test input_pizza method updates the order.

    Asserts:
        - One pizza is added to the order.
        - Total cost is updated correctly.
    """
    order = Order()
    order.input_pizza("thin", ["marinara"], "mozzarella", ["pineapple"])
    assert len(order.pizzas) == 1
    assert order.total_cost == 8


def test_order_paid():
    """
    Test order_paid method changes paid status.

    Asserts:
        - Payment flag is set to True after calling order_paid().
    """
    order = Order()
    order.order_paid()
    assert order.paid is True

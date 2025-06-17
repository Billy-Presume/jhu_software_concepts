"""
Module: test_integration.py
Author: Billy Presume
Created: 2025-06-17
Modified: 2025-06-17
Description: Contains integration tests that verify the behavior of multiple
Pizza objects within a single Order, ensuring total cost aggregation and
functional coordination between classes.
"""

import pytest
from src.order import Order

pytestmark = [pytest.mark.order, pytest.mark.pizza]


def test_multiple_pizzas_order():
    """
    Test that multiple pizzas in a single order are handled correctly.

    Asserts:
        - All pizzas are added to the order.
        - Total cost is the sum of individual pizza costs.
    """
    order = Order()
    order.input_pizza("thin", ["pesto"], "mozzarella", ["mushrooms"])  # $5 + $3 + $3 = 11
    order.input_pizza("thick", ["marinara"], "mozzarella", ["mushrooms"])  # $6 + $2 + $3 = 11
    assert order.total_cost == 22
    assert len(order.pizzas) == 2

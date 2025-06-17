"""
Module: test_pizza.py
Author: Billy Presume
Created: 2025-06-17
Modified: 2025-06-17
Description: Contains unit tests for the Pizza class. Verifies pizza
initialization, input validation, string representation, and cost
calculation.
"""

import pytest
from src.pizza import Pizza

pytestmark = pytest.mark.pizza


def test_pizza_init_valid():
    """
    Test that a pizza is correctly initialized with valid inputs.

    Asserts:
        - Crust, cheese, and cost are set properly.
    """
    pizza = Pizza("thin", ["marinara"], "mozzarella", ["pineapple"])
    assert pizza.crust == "thin"
    assert pizza.cheese == "mozzarella"
    assert pizza.cost() == 8


def test_pizza_invalid_cheese():
    """
    Test that an invalid cheese raises a ValueError.

    Asserts:
        - Pizza initialization fails with non-mozzarella cheese.
    """
    with pytest.raises(ValueError):
        Pizza("thin", ["marinara"], "cheddar", ["pineapple"])


def test_pizza_str():
    """
    Test the __str__ method for correct string formatting.

    Asserts:
        - The string includes the expected substrings like 'Cost'.
    """
    pizza = Pizza("thick", ["pesto"], "mozzarella", ["mushrooms"])
    assert "Cost:" in str(pizza)

"""
Module: order.py
Author: Billy Presume
Created: 2025-06-17
Modified: 2025-06-17
Description: Defines the Order class, which manages a collection of pizzas
for a single customer. Handles pizza input, total cost tracking, and
payment status for the order.
"""

from typing import List
from pizza import Pizza


class Order:
    """Represents a customer's pizza order."""

    def __init__(self) -> None:
        """Initialize an empty order with unpaid status."""
        self.pizzas: List[Pizza] = []
        self.total_cost: int = 0
        self.paid: bool = False

    def input_pizza(self, crust: str, sauces: List[str], cheese: str, toppings: List[str]) -> None:
        """
        Add a pizza to the order.

        Args:
            crust (str): Crust type.
            sauces (List[str]): Sauce types.
            cheese (str): Cheese type.
            toppings (List[str]): Toppings.
        """
        pizza = Pizza(crust, sauces, cheese, toppings)
        self.pizzas.append(pizza)
        self.total_cost += pizza.cost()

    def order_paid(self) -> None:
        """Mark the order as paid."""
        self.paid = True

    def __str__(self) -> str:
        """Return a string representation of the entire order."""
        order_str = "Customer Requested:\n"
        for pizza in self.pizzas:
            order_str += f"  {str(pizza)}\n"
        order_str += f"Total Cost: {self.total_cost}, Paid: {self.paid}"
        return order_str




# ---------------------------------------------------------------------------
# NOTE TO FRANCISCO:
# The following code block is included purely for replication purposes based
# on what I saw in the assignment description (page 5). I wasn’t sure whether
# Liv expected this to be implemented or submitted as part of the assignment,
# but I’ve added it here for completeness and demonstration.

# HOW TO RUN THE BELOW CODE:

# 1) Uncomment the print lines to see the example usage of the Order class
# 2) cd module_4/src/
# 3) python3 order.py
# ---------------------------------------------------------------------------

# Example usage of the Order class
order1 = Order()
order1.input_pizza("thin", ["pesto"], "mozzarella", ["mushrooms"])
order1.input_pizza("thick", ["marinara"], "mozzarella", [ "mushrooms"])
order1.order_paid()
# print(order1)


# Example usage of the Order class
order2 = Order()
order2.input_pizza("gluten_free", ["marinara"], "mozzarella", ["pineapple"])
order2.input_pizza("thin", ["liv_sauce", "pesto"], "mozzarella", ["pepperoni", "mushrooms"])
order2.order_paid()
# print(order2)
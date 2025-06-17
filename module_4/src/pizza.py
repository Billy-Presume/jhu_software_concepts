"""
Module: pizza.py
Author: Billy Presume
Created: 2025-06-17
Modified: 2025-06-17
Description: Defines the Pizza class used to create customizable pizza
objects with crust, sauce, cheese, and toppings. Includes logic to
calculate the total cost of a pizza based on selected options.
"""

from typing import List


class Pizza:
    """Represents a pizza with customizable options and dynamic cost calculation."""

    CRUST_COSTS = {
        "thin": 5,
        "thick": 6,
        "gluten_free": 8,
    }

    SAUCE_COSTS = {
        "marinara": 2,
        "pesto": 3,
        "liv_sauce": 5,
    }

    TOPPING_COSTS = {
        "pineapple": 1,
        "pepperoni": 2,
        "mushrooms": 3,
    }

    CHEESE = "mozzarella"

    def __init__(self, crust: str, sauces: List[str], cheese: str, toppings: List[str]) -> None:
        """
        Initialize a Pizza instance.

        Args:
            crust (str): Type of crust.
            sauces (List[str]): List of sauce types.
            cheese (str): Type of cheese (only mozzarella is valid).
            toppings (List[str]): List of toppings.

        Raises:
            ValueError: If input validation fails.
        """
        self.crust = crust.lower()
        self.sauces = [s.lower() for s in sauces]
        self.cheese = cheese.lower()
        self.toppings = [t.lower() for t in toppings]

        if self.cheese != self.CHEESE:
            raise ValueError("Only mozzarella cheese is allowed.")

        if self.crust not in self.CRUST_COSTS:
            raise ValueError(f"Invalid crust: {self.crust}")

        if not all(s in self.SAUCE_COSTS for s in self.sauces):
            raise ValueError("One or more sauces are invalid.")

        if not self.toppings or not all(t in self.TOPPING_COSTS for t in self.toppings):
            raise ValueError("Each pizza must have at least one valid topping.")

        self._cost = self.calculate_cost()

    def calculate_cost(self) -> int:
        """Calculate and return the total cost of the pizza."""
        return (
            self.CRUST_COSTS[self.crust] + sum(self.SAUCE_COSTS[s] for s in self.sauces) +
            sum(self.TOPPING_COSTS[t] for t in self.toppings)
        )

    def cost(self) -> int:
        """Return the cost of the pizza."""
        return self._cost

    def __str__(self) -> str:
        """Return a string representation of the pizza."""
        return (
            f"Crust: {self.crust}, Sauce: {self.sauces}, Cheese: {self.cheese}, "
            f"Toppings: {self.toppings}, Cost: {self._cost}"
        )
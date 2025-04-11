
from __future__ import annotations

import uuid
from decimal import Decimal

from goodmetrics.core.type_defs import Side


class Position:

    _side: Side
    _size: Decimal
    _price: Decimal
    _identifier: uuid.UUID
    
    def __init__(self, side: Side, size: Decimal = Decimal(0), price: Decimal = Decimal(0)) -> None:
        """
        Args:
            side (Side): The side of the position, either "BUY/LONG" or "SELL/SHORT".
            size (Decimal): The size of the position.
            price (Decimal): The price **per unit** of the position.
        """
        self._side = side
        self._size = size
        self._price = price

        self._identifier = uuid.uuid4()
    
    def __repr__(self) -> str:
        return f"Position(side={self.side}, size={self.size}, price={self.price})"

    def __str__(self) -> str:
        return f"Position(side={self.side}, size={self.size}, price={self.price})"
    
    def __eq__(self, other: Position) -> bool:
        if not isinstance(other, Position):
            return TypeError("Cannot compare Position with non-Position object.")
        
        return self.identifier == other.identifier
    
    def __ne__(self, other: Position) -> bool:
        if not isinstance(other, Position):
            return TypeError("Cannot compare Position with non-Position object.")
        
        return not self.__eq__(other)

    def equals_to(self, other: Position, strictly: bool = False) -> bool:
        """
        Compare two orders based on their attributes.
        If `strictly` is True, it will compare the identifiers as well.

        Args:
            other (Position): The other position to compare with.
            strictly (bool): If True, compare identifiers as well.
        
        Raises:
            TypeError: If `other` is not a Position instance.
        
        Returns:
            bool: True if the positions are equal, False otherwise.
        """
        if not isinstance(other, Position):
            return TypeError("Cannot compare Position with non-Position object.")
        
        if strictly:
            return self == other
        else:
            return (
                self.size == other.size
                and self.side == other.side
                and self.price == other.price
            )

    def add(self, other: Position) -> Position:
        """
        Add two positions together. 
        This will only work if the positions are on the same side.

        Args:
            other (Position): The other position to add.
        
        Raises:
            TypeError: If `other` is not a Position instance.
            ValueError: If the sides of the positions are different.

        Returns:
            Position: A new Position instance representing the combined position.
        """

        if not isinstance(other, Position):
            raise TypeError("Cannot add Position with non-Position object.")
        
        if self.side != other.side:
            raise ValueError("Cannot add positions with different sides.")
        
        self_side_weight = self.size / (self.size + other.size) # To calculate the weighted average price.
        return Position(
            side=self.side,
            size=self.size + other.size,
            price=self_side_weight * self.price + (1 - self_side_weight) * other.price
        )

    @property
    def size(self) -> Decimal:
        return self._size

    @size.setter
    def size(self, value: Decimal) -> None:
        if not isinstance(value, Decimal):
            raise TypeError("`size` must be a Decimal.")

        if value <= 0:
            raise ValueError("`size` must be greater than 0.")

        self._size = value

    @property
    def side(self) -> Side:
        return self._side

    @side.setter
    def side(self, value: Side) -> None:
        if value not in ("BUY/LONG", "SELL/SHORT"):
            raise ValueError("`side` must be either 'BUY/LONG' or 'SELL/SHORT'.")

        self._side = value

    @property
    def price(self) -> Decimal | None:
        return self._price

    @price.setter
    def price(self, value: Decimal | None) -> None:
        if value is not None and not isinstance(value, Decimal):
            raise TypeError("`price` must be a Decimal or None.")

        if value is not None and value <= 0:
            raise ValueError("`price` must be greater than 0.")

        self._price = value
    
    @property
    def identifier(self) -> uuid.UUID:
        return self._identifier

    # This setter is commented out to prevent changing the identifier after creation.
    # @property.setter
    # def identifier(self, value: uuid.UUID) -> None:
    #    pass

    @property
    def is_empty(self) -> bool:
        return self.size == 0

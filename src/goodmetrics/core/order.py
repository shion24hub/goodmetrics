from __future__ import annotations

import uuid
from abc import ABCMeta, abstractmethod
from decimal import Decimal
from typing import Type

from goodmetrics.core.type_defs import Side


# <-- Execution and Triggering Protocols -->
class ExecutionProtocolABC(metaclass=ABCMeta):
    @abstractmethod
    def check_execution(self, order: OrderABC) -> bool:
        pass


class TriggeringProtocolABC(metaclass=ABCMeta):
    @abstractmethod
    def check_triggering(self, order: OrderABC) -> bool:
        pass


# <-- Order Classes -->
class OrderABC(metaclass=ABCMeta):
    """
    Abstract base class for all order types.
    """

    @property
    @abstractmethod
    def size(self) -> Decimal:
        pass

    @property
    @abstractmethod
    def price(self) -> Decimal:
        pass

    @property
    @abstractmethod
    def side(self) -> Side:
        pass

    @property
    @abstractmethod
    def tp_price(self) -> Decimal | None:
        pass

    @property
    @abstractmethod
    def sl_price(self) -> Decimal | None:
        pass

    @property
    @abstractmethod
    def reduce_only(self) -> bool:
        pass

    @property
    @abstractmethod
    def trigger_price(self) -> Decimal | None:
        pass


class OrderBase(OrderABC):
    _size: Decimal
    _side: Side
    _price: Decimal | None
    _tp_price: Decimal | None
    _sl_price: Decimal | None
    _reduce_only: bool
    _trigger_price: Decimal | None
    _identifier: uuid.UUID

    def __init__(
        self,
        size: Decimal,
        side: Side,
        price: Decimal,
        tp_price: Decimal | None = None,
        sl_price: Decimal | None = None,
        trigger_price: Decimal | None = None,
        reduce_only: bool = False,
    ) -> None:
        """
        Args:
            size (Decimal): Size of the order.
            side (Side): Side of the order. Either 'BUY/LONG' or 'SELL/SHORT'.
            price (Decimal): Price of the order.
            tp_price (Decimal | None, optional): Take profit price. Defaults to None.
            sl_price (Decimal | None, optional): Stop loss price. Defaults to None.
            trigger_price (Decimal | None, optional): Trigger price for conditional orders. Defaults to None.
            reduce_only (bool, optional): If True, the order is a reduce-only order. Defaults to False.
        """

        self._size = size
        self._side = side
        self._price = price
        self._tp_price = tp_price
        self._sl_price = sl_price
        self._trigger_price = trigger_price
        self._reduce_only = reduce_only

        self._identifier = uuid.uuid4()  # Generate a unique identifier for the order.
        self._is_conditional = (
            False  # This will be set to True if `trigger_price` is not None.
        )

    def __repr__(self):
        return f"OrderBase(size={self.size}, side={self.side}, price={self.price}, tp_price={self.tp_price}, sl_price={self.sl_price}, trigger_price={self.trigger_price}), reduce_only={self.reduce_only}"

    def __str__(self):
        return f"OrderBase(size={self.size}, side={self.side}, price={self.price}, tp_price={self.tp_price}, sl_price={self.sl_price}, trigger_price={self.trigger_price}), reduce_only={self.reduce_only}"

    def __eq__(self, other: Type[OrderABC]) -> bool:
        """
        Compare two orders based on their identifiers.
        If you want to compare the attributes of the orders, use the `equals_to` method.
        """

        if not isinstance(other, Type[OrderABC]):
            return TypeError("Cannot compare OrderBase with non-OrderABC object.")

        return self.identifier == other.identifier

    def __ne__(self, other: Type[OrderABC]) -> bool:
        if not isinstance(other, Type[OrderABC]):
            return TypeError("Cannot compare OrderBase with non-OrderABC object.")

        return not self.__eq__(other)

    def equals_to(self, other: Type[OrderABC], strictly: bool = False) -> bool:
        """
        Compare two orders based on their attributes.
        If `strictly` is True, it will compare the identifiers as well.

        Args:
            other (OrderABC): The other order to compare with.
            strictly (bool): If True, compare identifiers as well.

        Raises:
            TypeError: If `other` is not an OrderABC instance.

        Returns:
            bool: True if the orders are equal, False otherwise.
        """
        if not isinstance(other, Type[OrderABC]):
            return TypeError("Cannot compare OrderBase with non-OrderABC object.")

        if strictly:
            return self == other
        else:
            return (
                self.size == other.size
                and self.price == other.price
                and self.side == other.side
                and self.tp_price == other.tp_price
                and self.sl_price == other.sl_price
                and self.trigger_price == other.trigger_price
                and self.reduce_only == other.reduce_only
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
    def tp_price(self) -> Decimal | None:
        return self._tp_price

    @tp_price.setter
    def tp_price(self, value: Decimal | None) -> None:
        if value is not None and not isinstance(value, Decimal):
            raise TypeError("`tp_price` must be a Decimal or None.")

        if value is not None and value <= 0:
            raise ValueError("`tp_price` must be greater than 0.")

        self._tp_price = value

    @property
    def sl_price(self) -> Decimal | None:
        return self._sl_price

    @sl_price.setter
    def sl_price(self, value: Decimal | None) -> None:
        if value is not None and not isinstance(value, Decimal):
            raise TypeError("`sl_price` must be a Decimal or None.")

        if value is not None and value <= 0:
            raise ValueError("`sl_price` must be greater than 0.")

        self._sl_price = value

    @property
    def reduce_only(self) -> bool:
        return self._reduce_only

    @reduce_only.setter
    def reduce_only(self, value: bool) -> None:
        if not isinstance(value, bool):
            raise TypeError("`reduce_only` must be a boolean.")

        self._reduce_only = value

    @property
    def trigger_price(self) -> Decimal | None:
        return self._trigger_price

    @trigger_price.setter
    def trigger_price(self, value: Decimal | None) -> None:
        if value is not None and not isinstance(value, Decimal):
            raise TypeError("`trigger_price` must be a Decimal or None.")

        if value is not None and value <= 0:
            raise ValueError("`trigger_price` must be greater than 0.")

        # If trigger_price is set(not None), set is_conditional to True
        if value is not None:
            self._is_conditional = True

        self._trigger_price = value

    @property
    def identifier(self) -> uuid.UUID:
        return self._identifier

    # This setter is commented out to prevent changing the identifier after creation.
    # @property.setter
    # def identifier(self, value: uuid.UUID) -> None:
    #    pass

    @property
    def is_conditional(self) -> bool:
        return self._is_conditional

    @is_conditional.setter
    def is_conditional(self, value: bool) -> None:
        if not isinstance(value, bool):
            raise TypeError("`is_conditional` must be a boolean.")

        self._is_conditional = value


class MarketOrder(OrderBase):
    """
    Market order class.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # Overridde the __repr__ method to include the class name
    def __repr__(self):
        return f"MarketOrder(size={self.size}, side={self.side}, price={self.price}, tp_price={self.tp_price}, sl_price={self.sl_price}, trigger_price={self.trigger_price}), reduce_only={self.reduce_only}"

    # Override the __str__ method to include the class name
    def __str__(self):
        return f"MarketOrder(size={self.size}, side={self.side}, price={self.price}, tp_price={self.tp_price}, sl_price={self.sl_price}, trigger_price={self.trigger_price}), reduce_only={self.reduce_only}"


class LimitOrder(OrderBase):
    """
    Limit order class.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # Override the __repr__ method to include the class name
    def __repr__(self):
        return f"LimitOrder(size={self.size}, side={self.side}, price={self.price}, tp_price={self.tp_price}, sl_price={self.sl_price}, trigger_price={self.trigger_price}), reduce_only={self.reduce_only}"

    # Override the __str__ method to include the class name
    def __str__(self):
        return f"LimitOrder(size={self.size}, side={self.side}, price={self.price}, tp_price={self.tp_price}, sl_price={self.sl_price}, trigger_price={self.trigger_price}), reduce_only={self.reduce_only}"


class OrderManager:
    """
    Order manager class to manage orders and conditional orders.
    """

    _initial_orders: list[Type[OrderABC]] | None
    _order_mapper: dict[uuid.UUID, Type[OrderABC]]
    _conditional_order_mapper: dict[uuid.UUID, Type[OrderABC]]
    _mutually_exclusive_order_mapper: dict[uuid.UUID, uuid.UUID]

    def __init__(self, initial_orders: list[Type[OrderABC]] | None = None):

        self._order_mapper: dict[uuid.UUID, Type[OrderABC]] = {}
        self._conditional_order_mapper: dict[uuid.UUID, Type[OrderABC]] = {}
        self._mutually_exclusive_order_mapper: dict[uuid.UUID, uuid.UUID] = {}

        if initial_orders is not None and not isinstance(initial_orders, list):
            raise TypeError("`initial_orders` must be a list of OrderABC instances.")
        
        initial_orders = initial_orders or []

        for order in initial_orders:
            # Check if the order is an instance of OrderABC in `add` method.
            if not order.is_conditional:
                self.add_to_order_mapper(order)
            else:
                self.add_to_conditional_order_mapper(order)
    
    def __repr__(self):
        pass

    def __str__(self):
        pass

    # TODO: Add a method to get dictionary of order_mapper and conditional_order_mapper.
    #       and delete the _order_mapper and _conditional_order_mapper properties.

    def add_to_order_mapper(self, order: Type[OrderABC]) -> None:
        """
        Add an order to the order mapper.

        Args:
            order (Type[OrderABC]): The order to add.
        Raises:
            TypeError: If the order is not an instance of OrderABC.
            ValueError: If the order is a conditional order.
        """
        if not isinstance(order, Type[OrderABC]):
            raise TypeError("`order` must be an instance of OrderABC.")

        if order.is_conditional:
            raise ValueError(
                "`order` is a conditional order. Use `add_to_conditional_order_mapper` method."
            )

        self._order_mapper[order.identifier] = order

    def add_to_conditional_order_mapper(self, order: Type[OrderABC]) -> None:
        """
        Add a conditional order to the conditional order mapper.

        Args:
            order (Type[OrderABC]): The conditional order to add.

        Raises:
            TypeError: If the order is not an instance of OrderABC.
            ValueError: If the order is not a conditional order.
        """

        if not isinstance(order, Type[OrderABC]):
            raise TypeError("`order` must be an instance of OrderABC.")

        if not order.is_conditional:
            raise ValueError(
                "`order` is not a conditional order. Use `add_to_orders_mapper` method."
            )

        self._conditional_order_mapper[order.identifier] = order

    def remove_from_order_mapper(self, identifier: uuid.UUID) -> None:
        """
        Remove an order from the order mapper.

        Args:
            identifier (uuid.UUID): The identifier of the order to remove.

        Raises:
            TypeError: If the identifier is not a UUID.
            KeyError: If the order is not found in the order mapper.
        """

        if not isinstance(identifier, uuid.UUID):
            raise TypeError("`identifier` must be a UUID.")

        if identifier in self._order_mapper:
            del self._order_mapper[identifier]
        else:
            raise KeyError(f"Order with identifier {identifier} not found.")

    def remove_from_conditional_order_mapper(self, identifier: uuid.UUID) -> None:
        """
        Remove a conditional order from the conditional order mapper.

        Args:
            identifier (uuid.UUID): The identifier of the conditional order to remove.

        Raises:
            TypeError: If the identifier is not a UUID.
            KeyError: If the conditional order is not found in the conditional order mapper.
        """
        if not isinstance(identifier, uuid.UUID):
            raise TypeError("`identifier` must be a UUID.")

        if identifier in self._conditional_order_mapper:
            del self._conditional_order_mapper[identifier]
        else:
            raise KeyError(f"Order with identifier {identifier} not found.")

    def add_mutually_exclusive_relationship(
        self, order1: Type[OrderABC], order2: Type[OrderABC]
    ) -> None:
        """
        Add a mutually exclusive relationship between two orders.
        This means that if one order is executed, the other will be canceled.
        **Only used for TP/SL orders.**

        Args:
            order1 (Type[OrderABC]): The first order.
            order2 (Type[OrderABC]): The second order.

        Raises:
            TypeError: If the orders are not instances of OrderABC.
            KeyError: If the orders are not found in the order manager.
        """

        if not isinstance(order1, Type[OrderABC]):
            raise TypeError("`order1` must be an instance of OrderABC.")

        if not isinstance(order2, Type[OrderABC]):
            raise TypeError("`order2` must be an instance of OrderABC.")

        if (
            order1.identifier not in self._order_mapper
            and order1.identifier not in self._conditional_order_mapper
        ):
            raise KeyError(
                f"Order with identifier {order1.identifier} not found. Use `add` method to add the order first."
            )

        if (
            order2.identifier not in self._order_mapper
            and order2.identifier not in self._conditional_order_mapper
        ):
            raise KeyError(
                f"Order with identifier {order2.identifier} not found. Use `add` method to add the order first."
            )

        self._mutually_exclusive_order_mapper[order1.identifier] = order2.identifier
        self._mutually_exclusive_order_mapper[order2.identifier] = order1.identifier

    def remove_mutually_exclusive_relationship(
        self, order1: Type[OrderABC], order2: Type[OrderABC]
    ) -> None:
        """
        Remove a mutually exclusive relationship between two orders.

        Args:
            order1 (Type[OrderABC]): The first order.
            order2 (Type[OrderABC]): The second order.
        Raises:
            TypeError: If the orders are not instances of OrderABC.
            KeyError: If the orders are not found in the order manager.
        """

        if not isinstance(order1, Type[OrderABC]):
            raise TypeError("`order1` must be an instance of OrderABC.")

        if not isinstance(order2, Type[OrderABC]):
            raise TypeError("`order2` must be an instance of OrderABC.")

        if order1.identifier not in self._mutually_exclusive_order_mapper:
            raise KeyError(f"Order with identifier {order1.identifier} not found.")

        if order2.identifier not in self._mutually_exclusive_order_mapper:
            raise KeyError(f"Order with identifier {order2.identifier} not found.")

        del self._mutually_exclusive_order_mapper[order1.identifier]
        del self._mutually_exclusive_order_mapper[order2.identifier]

    @classmethod
    def check_execution(
        cls, order: Type[OrderABC], protocol: Type[ExecutionProtocolABC]
    ) -> bool:
        """
        Check if an order should be executed based on the execution protocol.

        Args:
            order (Type[OrderABC]): The order to check.
            protocol (Type[ExecutionProtocolABC]): The execution protocol to use.

        Returns:
            bool: True if the order should be executed, False otherwise.
        """
        return protocol.check_execution(order)

    @classmethod
    def check_triggering(
        cls, order: Type[OrderABC], protocol: Type[TriggeringProtocolABC]
    ) -> bool:
        """
        Check if an order should be triggered based on the triggering protocol.

        Args:
            order (Type[OrderABC]): The order to check.
            protocol (Type[TriggeringProtocolABC]): The triggering protocol to use.

        Returns:
            bool: True if the order should be triggered, False otherwise.
        """
        return protocol.check_triggering(order)
    
    # OrderManager is not responsible for generating positions.
    # Move to position.py.
    # @classmethod
    # def generate_position(cls, order: Type[OrderABC]) -> Position:
    #     """
    #     Generate a position based on the order.
    #     TODO: Think about moving this to a Order class.

    #     Args:
    #         order (Type[OrderABC]): The order to generate a position from.

    #     Returns:
    #         Position: The generated position.
    #     """
    #     return Position(order.size, order.side, order.price)

    def generate_tp_sl_orders(
        self, order: Type[OrderABC]
    ) -> tuple[LimitOrder | None, MarketOrder | None]:
        """
        Generate take profit and stop loss orders based on the order.

        Args:
            order (Type[OrderABC]): The order to generate take profit and stop loss orders from.
        Returns:
            tuple[LimitOrder | None, MarketOrder | None]: The generated take profit and stop loss orders.
        """
        tp_order = None
        sl_order = None

        if order.tp_price is not None:
            tp_order = LimitOrder(
                size=order.size,
                side=order.side,
                price=order.tp_price,
                reduce_only=True,
            )
        if order.sl_price is not None:
            sl_order = LimitOrder(
                size=order.size,
                side=order.side,
                price=order.sl_price,
                reduce_only=True,
            )

        # Add mutually exclusive relationship between tp and sl orders
        if tp_order is not None and sl_order is not None:
            self.add_mutually_exclusive_relationship(tp_order, sl_order)

        return tp_order, sl_order

    def solve_conditional_orders_triggering(
        self, triggering_protocol: Type[TriggeringProtocolABC]
    ) -> list[uuid.UUID]:
        """
        Solve conditional orders based on the triggering protocol.
        This method checks if any conditional orders should be triggered based on the triggering protocol.
        If a conditional order is triggered, it is REMOVED from the conditional order mapper and ADDED to the order mapper.

        Args:
            triggering_protocol (Type[TriggeringProtocolABC]): The triggering protocol to use.

        Raises:
            TypeError: If the triggering protocol is not an instance of TriggeringProtocolABC.

        Returns:
            list[uuid.UUID]: A list of identifiers of the triggered orders.
        """

        triggered_ids: list[uuid.UUID] = []
        for identifier, order in list(self._conditional_order_mapper.items()):
            res = self.check_triggering(order, triggering_protocol)
            if res:
                triggered_ids.append(identifier)

        for identifier in triggered_ids:
            order = self._conditional_order_mapper[identifier]
            self.remove_from_conditional_order_mapper(identifier)
            self.add_to_order_mapper(order)

        return triggered_ids

    def solve_orders_execution(
        self, execution_protocol: Type[ExecutionProtocolABC]
    ) -> list[uuid.UUID]:
        """
        Solve orders based on the execution protocol.
        This method checks if any orders should be executed based on the execution protocol.
        If an order is executed, it is REMOVED from the order mapper.

        Args:
            execution_protocol (Type[ExecutionProtocolABC]): The execution protocol to use.

        Raises:
            TypeError: If the execution protocol is not an instance of ExecutionProtocolABC.

        Returns:
            list[uuid.UUID]: A list of identifiers of the executed orders.
        """

        executed_ids: list[uuid.UUID] = []
        for identifier, order in list(self._order_mapper.items()):
            res = self.check_execution(order, execution_protocol)
            if res:
                executed_ids.append(identifier)

        for identifier in executed_ids:
            order = self._order_mapper[identifier]
            self.remove_from_order_mapper(identifier)

        return executed_ids

    @property
    def order_mapper(self) -> dict[uuid.UUID, Type[OrderABC]]:
        return self._order_mapper

    @property
    def conditional_order_mapper(self) -> dict[uuid.UUID, Type[OrderABC]]:
        return self._conditional_order_mapper

    @property
    def exclusive_order_mapper(self) -> dict[uuid.UUID, uuid.UUID]:
        return self._exclusive_order_mapper

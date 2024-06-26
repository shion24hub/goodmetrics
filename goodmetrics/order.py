from __future__ import annotations
from dataclasses import dataclass
from typing import Literal, Optional

Side = Literal['Buy/Long', 'Sell/Short']


@dataclass
class MarketOrder:
    side: Side
    size: int

    reduce_only: bool = False
    stop_loss: Optional[StopOrder] = None
    take_profit: Optional[LimitOrder] = None
    
    def __post_init__(self):
        if self.size <= 0:
            raise ValueError('`size` must be positive')
        if self.side not in ['Buy/Long', 'Sell/Short']:
            raise ValueError('`side` must be either `Buy/Long` or `Sell/Short`')
        
        self.position = self.size if self.side == 'Buy/Long' else -self.size
        
    def is_valid(self, price: float) -> bool:
        return True
    
    def is_triggered(self, high: float, low: float) -> bool:
        return True
    
    def entry_price(self, price: float) -> float:
        return price


@dataclass
class LimitOrder:
    side: Side
    size: float
    target_price: float

    reduce_only: bool = False
    stop_loss: Optional[StopOrder] = None
    take_profit: Optional[LimitOrder] = None
    
    def __post_init__(self):
        if self.size <= 0:
            raise ValueError('`size` must be positive')
        if self.side not in ['Buy/Long', 'Sell/Short']:
            raise ValueError('`side` must be either `Buy/Long` or `Sell/Short')
        if self.target_price <= 0:
            raise ValueError('`price` must be positive')
        
        self.position = self.size if self.side == 'Buy/Long' else -self.size
        
    def is_valid(self, price: float) -> bool:
        if self.side == 'Buy/Long':
            return price >= self.target_price
        else:
            return price <= self.target_price
    
    def is_triggered(self, high: float, low: float) -> bool:
        if self.side == 'Buy/Long':
            return low <= self.target_price
        else:
            return high >= self.target_pric
        
    def entry_price(self, price: float) -> float:
        return self.target_price


@dataclass
class StopOrder:
    side: Side
    size: float
    target_price: float

    reduce_only: bool = False
    stop_loss: Optional[StopOrder] = None
    take_profit: Optional[LimitOrder] = None

    def __post_init__(self):
        if self.size <= 0:
            raise ValueError('`size` must be positive')
        if self.side not in ['Buy/Long', 'Sell/Short']:
            raise ValueError('`side` must be either `Buy/Long` or `Sell/Short')
        if self.target_price <= 0:
            raise ValueError('`price` must be positive')
        
        self.position = self.size if self.side == 'Buy/Long' else -self.size
    
    def is_valid(self, price: float) -> bool:
        if self.side == 'Buy/Long':
            return price <= self.target_price
        else:
            return price >= self.target_price
    
    def is_triggered(self, high: float, low: float) -> bool:
        if self.side == 'Buy/Long':
            return low >= self.target_price
        else:
            return high <= self.target_price
        
    def entry_price(self, price: float) -> float:
        return self.target_price


from dataclasses import dataclass
from typing import Literal, Optional

Side = Literal['Buy/Long', 'Sell/Short']


@dataclass
class MarketOrder:
    side: Side
    size: int

    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None
    
    def __post_init__(self):
        if self.size <= 0:
            raise ValueError('`size` must be positive')
        if self.side not in ['Buy/Long', 'Sell/Short']:
            raise ValueError('`side` must be either `Buy/Long` or `Sell/Short`')
        if self.stop_loss is not None and self.stop_loss <= 0:
            raise ValueError('`stop_loss` must be positive')
        if self.take_profit is not None and self.take_profit <= 0:
            raise ValueError('`take_profit` must be positive')
        
    def is_valid(self, price: float) -> bool:
        return True
    
    def is_triggered(self, high: float, low: float) -> bool:
        return True


@dataclass
class LimitOrder:
    side: Side
    size: float
    target_price: float

    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None
    
    def __post_init__(self):
        if self.size <= 0:
            raise ValueError('`size` must be positive')
        if self.side not in ['Buy/Long', 'Sell/Short']:
            raise ValueError('`side` must be either `Buy/Long` or `Sell/Short')
        if self.target_price <= 0:
            raise ValueError('`price` must be positive')
        if self.stop_loss is not None and self.stop_loss <= 0:
            raise ValueError('`stop_loss` must be positive')
        if self.take_profit is not None and self.take_profit <= 0:
            raise ValueError('`take_profit` must be positive')
        
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


@dataclass
class StopOrder:
    side: Side
    size: float
    target_price: float

    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None

    def __post_init__(self):
        if self.size <= 0:
            raise ValueError('`size` must be positive')
        if self.side not in ['Buy/Long', 'Sell/Short']:
            raise ValueError('`side` must be either `Buy/Long` or `Sell/Short')
        if self.target_price <= 0:
            raise ValueError('`price` must be positive')
        if self.stop_loss is not None and self.stop_loss <= 0:
            raise ValueError('`stop_loss` must be positive')
        if self.take_profit is not None and self.take_profit <= 0:
            raise ValueError('`take_profit` must be positive')
    
    def is_valid(self, price: float) -> bool:
        if self.side == 'Buy/Long':
            return price <= self.target_price
        else:
            return price >= self.target_price
    
    def is_triggered(self, high: float, low: float) -> bool:
        if self.side == 'Buy/Long':
            return low >= self.target_price
        else:
            return high <= self.target_pric


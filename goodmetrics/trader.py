from __future__ import annotations
from datetime import datetime
from dataclasses import dataclass

from data import OHLCV
from order import MarketOrder, LimitOrder, StopOrder

Order = MarketOrder | LimitOrder | StopOrder
Plan = dict[datetime, list[Order]]


class Market:
    def __init__(self, ohlcv: OHLCV) -> None:
        self.ohlcv = ohlcv

        self.traders: list[Trader] = []
        self.exchange_mapper: dict[Trader, Exchange] = {}

    def swallow(self, trader: Trader) -> None:
        exchange = Exchange()
        self.traders.append(trader)
        self.exchange_mapper[trader] = exchange


    def spit(self, *traders: Trader) -> None:
        for trader in traders:
            self.traders.remove(trader)
    
    def run_one(self, trader: Trader) -> None:
        dts = self.ohlcv.data.index.values
        highs = self.ohlcv.data['high'].values
        lows = self.ohlcv.data['low'].values
        closes = self.ohlcv.data['close'].values

        for dt, hi, lo, cl in zip(dts, highs, lows, closes):
            order = trader.act(dt)
            self.exchange.place(trader, order)
            self.exchange.check(trader, hi, lo, cl)
    
    def run(self) -> None:
        for trader in self.traders:
            self.run_one(trader)


@dataclass
class Ledger:
    initial_cash: float

    def __post_init__(self):
        if self.initial_cash <= 0:
            raise ValueError('`initial_cash` must be positive')
        
        self.cash_history = [self.initial_cash]


class Exchange:
    def __init__(self) -> None:
        pass

    def register(self, trader: Trader) -> None:
        pass

    def place(self, order: Order) -> None:
        pass

    def check(self) -> None:
        pass


class Trader:
    def __init__(self, plan: Plan, cash: float = 1_000_000_000_000.0) -> None:
        self.plan = plan
        self.cash = cash

    def act(self, dt: datetime) -> Order:
        order = self.plan.get(dt, [])

    def use(self, exchange: Exchange) -> None:
        pass




if __name__ == '__main__':
    pass

    # import pandas as pd

    # data = pd.read_csv(...)
    # plan1 = {
    #     datetime(2023, 1, 1): [MarketOrder('Buy/Long', 1)],
    #     datetime(2024, 1, 1): [MarketOrder('Sell/Short', 1)]
    # }
    # plan2 = {
    #     datetime(2023, 1, 2): [MarketOrder('Buy/Long', 1)],
    #     datetime(2024, 1, 2): [MarketOrder('Sell/Short', 1)]
    # }


    # cash = 1_000_000_000_000

    # ohlcv = OHLCV(data)
    # market = Market(ohlcv)

    # trader1 = Trader(cash, plan1)
    # trader2 = Trader(cash, plan2)

    # market.swallow(trader1, trader2)
    # market.run()


    # position: float = 0
    # next_orders: list[Order] = []
    # waiting_orders: list[Order] = []

    # for dt, hi, lo, cl in zip(self.ohlcv.data.index, highs, lows, closes):

    #     waiting_orders.extend(next_orders)
        
    #     # get orders for this datetime and append to next_orders
    #     orders = self.plan.get(dt, [])
    #     for order in orders:
    #         if order.is_valid(cl):
    #             next_orders.append(order)

    #     # check if any waiting orders are triggered
    #     for order in waiting_orders:
    #         if order.is_triggered(hi, lo):
    #             position += order.position
    #             waiting_orders.remove(order)

    #             if order.take_profit is not None:
    #                 next_orders.append(order.take_profit)

    #             if order.stop_loss is not None:
    #                 next_orders.append(order.stop_loss)


            

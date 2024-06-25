from datetime import datetime

from data import OHLCV
from order import MarketOrder, LimitOrder, StopOrder

Order = MarketOrder | LimitOrder | StopOrder
Plan = dict[datetime, list[Order]]

class Trader:
    def __init__(self, ohlcv: OHLCV, plan: Plan) -> None:
        self.ohlcv = ohlcv
        self.plan = plan

    def run(self) -> None:
        highs = self.ohlcv.data['high']
        lows = self.ohlcv.data['low']
        closes = self.ohlcv.data['close']

        # tracking
        next_orders: list[Order] = []
        waiting_orders: list[Order] = []
        open_orders: list[Order] = []
        chained_orders: dict[Order, Order] = {}

        for dt, hi, lo, cl in zip(self.ohlcv.data.index, highs, lows, closes):

            waiting_orders.extend(next_orders)
            
            # get orders for this datetime and append to next_orders
            orders = self.plan.get(dt, [])
            for order in orders:
                if order.is_valid(cl):
                    next_orders.append(order)
                    
                    if order.stop_loss is not None or order.take_profit is not None:
                        chained_orders[order] = order

            # check if any waiting orders are triggered
            for order in waiting_orders:
                if order.is_triggered(cl):
                    open_orders.append(order)
                    waiting_orders.remove(order)

                    
                    
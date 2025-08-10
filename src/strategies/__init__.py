"""
Trading Strategies Module

Collection of trading strategies for portfolio backtesting.
"""

from .base_strategy import BaseStrategy
from .buy_and_hold import BuyAndHoldStrategy

__all__ = ["BaseStrategy", "BuyAndHoldStrategy"] 
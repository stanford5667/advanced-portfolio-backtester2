"""
Advanced Portfolio Backtester

A comprehensive portfolio backtesting framework with advanced analysis tools,
risk metrics, and visualization capabilities.
"""

__version__ = "0.1.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

from .backtester import PortfolioBacktester
from .strategies import BaseStrategy, BuyAndHoldStrategy
from .analytics import PerformanceAnalyzer

__all__ = [
    "PortfolioBacktester",
    "BaseStrategy", 
    "BuyAndHoldStrategy",
    "PerformanceAnalyzer",
] 
"""
Buy and Hold Strategy

Simple buy and hold strategy that buys all assets and holds them.
"""

import pandas as pd
import numpy as np
from .base_strategy import BaseStrategy


class BuyAndHoldStrategy(BaseStrategy):
    """
    Buy and Hold Strategy.
    
    This strategy buys all assets at the beginning and holds them
    throughout the entire backtest period.
    """
    
    def __init__(self, **kwargs):
        """
        Initialize the buy and hold strategy.
        
        Args:
            **kwargs: Strategy parameters (none for buy and hold)
        """
        super().__init__(**kwargs)
    
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Generate buy and hold signals.
        
        Args:
            data: DataFrame with price data (index: dates, columns: symbols)
            
        Returns:
            DataFrame with trading signals (1 for all assets on all dates)
        """
        # Create signals DataFrame with same shape as data
        signals = pd.DataFrame(index=data.index, columns=data.columns)
        
        # Set all signals to 1 (buy and hold)
        signals = signals.fillna(1)
        
        return signals
    
    def __str__(self) -> str:
        """String representation of the strategy."""
        return "BuyAndHoldStrategy" 
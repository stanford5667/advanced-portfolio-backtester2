"""
Base Strategy Class

Abstract base class for all trading strategies.
"""

from abc import ABC, abstractmethod
import pandas as pd
from typing import Dict, Any


class BaseStrategy(ABC):
    """
    Abstract base class for trading strategies.
    
    All trading strategies should inherit from this class and implement
    the generate_signals method.
    """
    
    def __init__(self, **kwargs):
        """
        Initialize the strategy with parameters.
        
        Args:
            **kwargs: Strategy-specific parameters
        """
        self.params = kwargs
        self.name = self.__class__.__name__
    
    @abstractmethod
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Generate trading signals based on the input data.
        
        Args:
            data: DataFrame with price data (index: dates, columns: symbols)
            
        Returns:
            DataFrame with trading signals (1: buy, 0: hold, -1: sell)
        """
        pass
    
    def get_parameters(self) -> Dict[str, Any]:
        """
        Get strategy parameters.
        
        Returns:
            Dictionary with strategy parameters
        """
        return self.params
    
    def set_parameters(self, **kwargs):
        """
        Set strategy parameters.
        
        Args:
            **kwargs: New parameter values
        """
        self.params.update(kwargs)
    
    def __str__(self) -> str:
        """String representation of the strategy."""
        params_str = ", ".join([f"{k}={v}" for k, v in self.params.items()])
        return f"{self.name}({params_str})" 
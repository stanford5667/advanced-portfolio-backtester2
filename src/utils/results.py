"""
Backtest Results

Container for backtest results and performance metrics.
"""

from typing import Dict, Any


class BacktestResults:
    """Container for backtest results and performance metrics."""
    
    def __init__(self, **kwargs):
        """Initialize results with performance metrics."""
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert results to dictionary."""
        return {
            'final_value': self.final_value,
            'total_return': self.total_return,
            'annualized_return': self.annualized_return,
            'sharpe_ratio': self.sharpe_ratio,
            'max_drawdown': self.max_drawdown,
            'volatility': self.volatility,
            'sortino_ratio': getattr(self, 'sortino_ratio', 0.0),
            'calmar_ratio': getattr(self, 'calmar_ratio', 0.0),
            'var_95': getattr(self, 'var_95', 0.0),
            'weights': self.weights
        } 
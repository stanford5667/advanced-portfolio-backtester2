"""
Basic Tests

Simple tests to verify the installation and basic functionality.
"""

import pytest
import sys
from pathlib import Path

# Add src to path for testing
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))


def test_imports():
    """Test that all modules can be imported."""
    try:
        from backtester import PortfolioBacktester
        from strategies import BaseStrategy, BuyAndHoldStrategy
        from analytics import PerformanceAnalyzer
        assert True
    except ImportError as e:
        pytest.fail(f"Import failed: {e}")


def test_buy_and_hold_strategy():
    """Test the buy and hold strategy."""
    from strategies import BuyAndHoldStrategy
    import pandas as pd
    
    # Create sample data
    dates = pd.date_range('2020-01-01', '2020-12-31', freq='D')
    data = pd.DataFrame({
        'AAPL': [100 + i * 0.1 for i in range(len(dates))],
        'GOOGL': [200 + i * 0.2 for i in range(len(dates))]
    }, index=dates)
    
    # Test strategy
    strategy = BuyAndHoldStrategy()
    signals = strategy.generate_signals(data)
    
    # Check that all signals are 1 (buy and hold)
    assert (signals == 1).all().all()
    assert signals.shape == data.shape


def test_performance_analyzer():
    """Test the performance analyzer."""
    from analytics import PerformanceAnalyzer
    import pandas as pd
    import numpy as np
    
    # Create sample data
    dates = pd.date_range('2020-01-01', '2020-12-31', freq='D')
    portfolio_values = pd.Series(
        [100000 + i * 100 for i in range(len(dates))],
        index=dates
    )
    
    weights = pd.DataFrame({
        'AAPL': [0.5] * len(dates),
        'GOOGL': [0.5] * len(dates)
    }, index=dates)
    
    # Test analyzer
    analyzer = PerformanceAnalyzer()
    results = analyzer.calculate_metrics(portfolio_values, weights, 100000)
    
    # Check that results have expected attributes
    assert hasattr(results, 'total_return')
    assert hasattr(results, 'sharpe_ratio')
    assert hasattr(results, 'max_drawdown')
    assert hasattr(results, 'weights')


if __name__ == '__main__':
    # Run basic tests
    test_imports()
    test_buy_and_hold_strategy()
    test_performance_analyzer()
    print("✅ All basic tests passed!") 
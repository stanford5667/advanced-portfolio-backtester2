"""
Portfolio Backtester

Main backtesting engine for portfolio analysis.
"""

import pandas as pd
import numpy as np
from datetime import datetime
from typing import List, Dict, Any
import yfinance as yf

from src.strategies import BaseStrategy
from src.analytics import PerformanceAnalyzer
from src.utils.results import BacktestResults


class PortfolioBacktester:
    """
    Main portfolio backtesting engine.
    
    This class handles the core backtesting logic including data fetching,
    strategy execution, and performance calculation.
    """
    
    def __init__(
        self,
        symbols: List[str],
        start_date: str,
        end_date: str,
        initial_capital: float = 100000,
        rebalance_frequency: str = 'monthly'
    ):
        """
        Initialize the portfolio backtester.
        
        Args:
            symbols: List of stock symbols to backtest
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            initial_capital: Initial portfolio value
            rebalance_frequency: How often to rebalance ('daily', 'weekly', 'monthly')
        """
        self.symbols = symbols
        self.start_date = start_date
        self.end_date = end_date
        self.initial_capital = initial_capital
        self.rebalance_frequency = rebalance_frequency
        
        self.data = None
        self.portfolio_values = None
        self.weights_history = None
        
    def fetch_data(self) -> pd.DataFrame:
        """
        Fetch historical price data for the symbols.
        
        Returns:
            DataFrame with historical prices
        """
        print(f"📥 Fetching data for {', '.join(self.symbols)}...")
        
        try:
            # Download data using yfinance
            data = yf.download(
                self.symbols,
                start=self.start_date,
                end=self.end_date,
                progress=False
            )
            
            # Handle single symbol case
            if len(self.symbols) == 1:
                data = pd.DataFrame(data['Adj Close'])
                data.columns = self.symbols
            else:
                # For multiple symbols, extract only the Adj Close column
                if 'Adj Close' in data.columns:
                    data = data['Adj Close']
                else:
                    # Fallback to Close if Adj Close is not available
                    data = data['Close']
            
            # Forward fill missing values
            data = data.ffill()
            
            print(f"✅ Downloaded {len(data)} days of data")
            return data
            
        except Exception as e:
            print(f"❌ Error fetching data: {e}")
            # Return sample data for demonstration
            return self._generate_sample_data()
    
    def _generate_sample_data(self) -> pd.DataFrame:
        """Generate sample data for demonstration purposes."""
        print("⚠️  Using sample data for demonstration...")
        
        # Generate sample dates
        start = pd.to_datetime(self.start_date)
        end = pd.to_datetime(self.end_date)
        dates = pd.date_range(start=start, end=end, freq='D')
        
        # Generate sample prices with some realistic patterns
        np.random.seed(42)  # For reproducible results
        
        data = {}
        for symbol in self.symbols:
            # Start with a base price
            base_price = 100 + np.random.randint(50, 200)
            
            # Generate daily returns with some trend and volatility
            daily_returns = np.random.normal(0.0005, 0.02, len(dates))
            
            # Add some trend
            trend = np.linspace(0, 0.1, len(dates))
            daily_returns += trend / len(dates)
            
            # Calculate cumulative prices
            prices = base_price * np.exp(np.cumsum(daily_returns))
            data[symbol] = prices
        
        return pd.DataFrame(data, index=dates)
    
    def run(self, strategy: BaseStrategy) -> 'BacktestResults':
        """
        Run the backtest with the given strategy.
        
        Args:
            strategy: Strategy object to use for the backtest
            
        Returns:
            BacktestResults object with performance metrics
        """
        print("🔄 Running backtest...")
        
        # Fetch data if not already done
        if self.data is None:
            self.data = self.fetch_data()
        
        # Generate signals from strategy
        signals = strategy.generate_signals(self.data)
        
        # Calculate portfolio weights
        weights = self._calculate_weights(signals)
        
        # Calculate portfolio returns
        returns = self._calculate_returns(weights)
        
        # Calculate portfolio values
        portfolio_values = self._calculate_portfolio_values(returns)
        
        # Store results
        self.portfolio_values = portfolio_values
        self.weights_history = weights
        
        # Calculate performance metrics
        analyzer = PerformanceAnalyzer()
        results = analyzer.calculate_metrics(
            portfolio_values=portfolio_values,
            weights=weights,
            initial_capital=self.initial_capital
        )
        
        print("✅ Backtest completed!")
        return results
    
    def _calculate_weights(self, signals: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate portfolio weights based on signals.
        
        Args:
            signals: DataFrame with buy/sell signals
            
        Returns:
            DataFrame with portfolio weights
        """
        # Simple equal weight allocation for now
        weights = pd.DataFrame(index=signals.index, columns=signals.columns)
        
        for date in signals.index:
            # Get active positions (where signal > 0)
            active_positions = signals.loc[date] > 0
            
            if active_positions.sum() > 0:
                # Equal weight allocation
                weight = 1.0 / active_positions.sum()
                weights.loc[date] = active_positions * weight
            else:
                # All cash if no positions
                weights.loc[date] = 0.0
        
        return weights
    
    def _calculate_returns(self, weights: pd.DataFrame) -> pd.Series:
        """
        Calculate portfolio returns based on weights.
        
        Args:
            weights: DataFrame with portfolio weights
            
        Returns:
            Series with portfolio returns
        """
        # Calculate asset returns
        asset_returns = self.data.pct_change()
        
        # Calculate portfolio returns
        portfolio_returns = (weights.shift(1) * asset_returns).sum(axis=1)
        
        return portfolio_returns.ffill().fillna(0)
    
    def _calculate_portfolio_values(self, returns: pd.Series) -> pd.Series:
        """
        Calculate portfolio values over time.
        
        Args:
            returns: Series with portfolio returns
            
        Returns:
            Series with portfolio values
        """
        # Calculate cumulative returns
        cumulative_returns = (1 + returns).cumprod()
        
        # Calculate portfolio values
        portfolio_values = self.initial_capital * cumulative_returns
        
        return portfolio_values 
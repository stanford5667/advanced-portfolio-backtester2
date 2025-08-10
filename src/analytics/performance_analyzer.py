"""
Performance Analyzer

Calculates various performance metrics and risk measures for portfolios.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any
from src.utils.results import BacktestResults


class PerformanceAnalyzer:
    """
    Performance analyzer for calculating portfolio metrics.
    
    This class provides methods to calculate various performance metrics
    including returns, risk measures, and ratios.
    """
    
    def __init__(self, risk_free_rate: float = 0.02):
        """
        Initialize the performance analyzer.
        
        Args:
            risk_free_rate: Annual risk-free rate (default: 2%)
        """
        self.risk_free_rate = risk_free_rate
    
    def calculate_metrics(
        self,
        portfolio_values: pd.Series,
        weights: pd.DataFrame,
        initial_capital: float
    ) -> BacktestResults:
        """
        Calculate comprehensive performance metrics.
        
        Args:
            portfolio_values: Series with portfolio values over time
            weights: DataFrame with portfolio weights over time
            initial_capital: Initial portfolio value
            
        Returns:
            BacktestResults object with all calculated metrics
        """
        # Calculate basic metrics
        final_value = portfolio_values.iloc[-1]
        total_return = (final_value - initial_capital) / initial_capital
        
        # Calculate returns
        returns = portfolio_values.pct_change().fillna(0)
        
        # Calculate annualized metrics
        days = len(portfolio_values)
        years = days / 252  # Assuming 252 trading days per year
        
        annualized_return = (1 + total_return) ** (1 / years) - 1
        volatility = returns.std() * np.sqrt(252)
        
        # Calculate risk-adjusted metrics
        excess_returns = returns - self.risk_free_rate / 252
        sharpe_ratio = self._calculate_sharpe_ratio(excess_returns)
        sortino_ratio = self._calculate_sortino_ratio(returns)
        
        # Calculate drawdown
        max_drawdown = self._calculate_max_drawdown(portfolio_values)
        
        # Calculate additional metrics
        calmar_ratio = self._calculate_calmar_ratio(annualized_return, max_drawdown)
        var_95 = self._calculate_var(returns, 0.05)
        
        # Get final weights
        final_weights = weights.iloc[-1].to_dict()
        
        # Create results object
        results = BacktestResults(
            final_value=final_value,
            total_return=total_return,
            annualized_return=annualized_return,
            sharpe_ratio=sharpe_ratio,
            sortino_ratio=sortino_ratio,
            max_drawdown=max_drawdown,
            volatility=volatility,
            calmar_ratio=calmar_ratio,
            var_95=var_95,
            weights=final_weights
        )
        
        return results
    
    def _calculate_sharpe_ratio(self, excess_returns: pd.Series) -> float:
        """
        Calculate Sharpe ratio.
        
        Args:
            excess_returns: Series with excess returns
            
        Returns:
            Sharpe ratio
        """
        if excess_returns.std() == 0:
            return 0.0
        
        return (excess_returns.mean() * 252) / (excess_returns.std() * np.sqrt(252))
    
    def _calculate_sortino_ratio(self, returns: pd.Series) -> float:
        """
        Calculate Sortino ratio.
        
        Args:
            returns: Series with returns
            
        Returns:
            Sortino ratio
        """
        # Calculate downside returns
        downside_returns = returns[returns < 0]
        
        if len(downside_returns) == 0:
            return 0.0
        
        # Calculate downside deviation
        downside_deviation = downside_returns.std() * np.sqrt(252)
        
        if downside_deviation == 0:
            return 0.0
        
        # Calculate excess return
        excess_return = (returns.mean() * 252) - self.risk_free_rate
        
        return excess_return / downside_deviation
    
    def _calculate_max_drawdown(self, portfolio_values: pd.Series) -> float:
        """
        Calculate maximum drawdown.
        
        Args:
            portfolio_values: Series with portfolio values
            
        Returns:
            Maximum drawdown as a percentage
        """
        # Calculate running maximum
        running_max = portfolio_values.expanding().max()
        
        # Calculate drawdown
        drawdown = (portfolio_values - running_max) / running_max
        
        # Return maximum drawdown
        return abs(drawdown.min())
    
    def _calculate_calmar_ratio(self, annualized_return: float, max_drawdown: float) -> float:
        """
        Calculate Calmar ratio.
        
        Args:
            annualized_return: Annualized return
            max_drawdown: Maximum drawdown
            
        Returns:
            Calmar ratio
        """
        if max_drawdown == 0:
            return 0.0
        
        return annualized_return / max_drawdown
    
    def _calculate_var(self, returns: pd.Series, confidence_level: float) -> float:
        """
        Calculate Value at Risk.
        
        Args:
            returns: Series with returns
            confidence_level: Confidence level (e.g., 0.05 for 95% VaR)
            
        Returns:
            Value at Risk as a percentage
        """
        return abs(np.percentile(returns, confidence_level * 100))
    
    def generate_summary_report(self, results: BacktestResults) -> str:
        """
        Generate a text summary report.
        
        Args:
            results: BacktestResults object
            
        Returns:
            Formatted summary report
        """
        report = f"""
Portfolio Performance Summary
============================

Returns:
- Total Return: {results.total_return:.2%}
- Annualized Return: {results.annualized_return:.2%}

Risk Metrics:
- Volatility: {results.volatility:.2%}
- Maximum Drawdown: {results.max_drawdown:.2%}
- Value at Risk (95%): {results.var_95:.2%}

Risk-Adjusted Metrics:
- Sharpe Ratio: {results.sharpe_ratio:.2f}
- Sortino Ratio: {results.sortino_ratio:.2f}
- Calmar Ratio: {results.calmar_ratio:.2f}

Portfolio Composition:
"""
        
        for symbol, weight in results.weights.items():
            report += f"- {symbol}: {weight:.2%}\n"
        
        return report 
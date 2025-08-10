#!/usr/bin/env python3
"""
Basic Example - Advanced Portfolio Backtester

This example demonstrates how to run a simple buy-and-hold portfolio backtest.
"""

import sys
import os
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

try:
    from backtester import PortfolioBacktester
    from strategies import BuyAndHoldStrategy
    from analytics import PerformanceAnalyzer
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("💡 Make sure you have installed the package: pip install -e .")
    sys.exit(1)


def main():
    """Run a basic portfolio backtest example"""
    print("🚀 Advanced Portfolio Backtester - Basic Example")
    print("=" * 50)
    
    # Configuration
    symbols = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA']
    start_date = '2020-01-01'
    end_date = '2023-12-31'
    initial_capital = 100000
    
    print(f"📊 Portfolio: {', '.join(symbols)}")
    print(f"📅 Period: {start_date} to {end_date}")
    print(f"💰 Initial Capital: ${initial_capital:,.2f}")
    print()
    
    try:
        # Initialize backtester
        print("🔧 Initializing backtester...")
        backtester = PortfolioBacktester(
            symbols=symbols,
            start_date=start_date,
            end_date=end_date,
            initial_capital=initial_capital
        )
        
        # Run backtest
        print("⚡ Running backtest...")
        results = backtester.run(BuyAndHoldStrategy())
        
        # Display results
        print("\n📈 Results Summary:")
        print("-" * 30)
        print(f"Final Portfolio Value: ${results.final_value:,.2f}")
        print(f"Total Return: {results.total_return:.2%}")
        print(f"Annualized Return: {results.annualized_return:.2%}")
        print(f"Sharpe Ratio: {results.sharpe_ratio:.2f}")
        print(f"Maximum Drawdown: {results.max_drawdown:.2%}")
        print(f"Volatility: {results.volatility:.2%}")
        
        # Additional metrics
        print("\n📊 Risk Metrics:")
        print("-" * 30)
        print(f"Sortino Ratio: {results.sortino_ratio:.2f}")
        print(f"Calmar Ratio: {results.calmar_ratio:.2f}")
        print(f"Value at Risk (95%): {results.var_95:.2%}")
        
        # Portfolio composition
        print("\n🏗️  Portfolio Composition:")
        print("-" * 30)
        for symbol, weight in results.weights.items():
            print(f"{symbol}: {weight:.2%}")
        
        print("\n✅ Backtest completed successfully!")
        print("\n💡 Next steps:")
        print("1. Try different strategies")
        print("2. Experiment with different time periods")
        print("3. Add more sophisticated risk metrics")
        print("4. Use the CLI: python -m src.main sample")
        
    except Exception as e:
        print(f"❌ Error during backtest: {e}")
        print("\n💡 Troubleshooting:")
        print("1. Check your internet connection (for data download)")
        print("2. Verify the stock symbols are valid")
        print("3. Ensure all dependencies are installed")
        return 1
    
    return 0


if __name__ == '__main__':
    exit(main()) 
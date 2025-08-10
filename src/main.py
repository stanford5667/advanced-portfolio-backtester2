#!/usr/bin/env python3
"""
Advanced Portfolio Backtester CLI

Command-line interface for running portfolio backtests and generating reports.
"""

import click
import json
from datetime import datetime
from pathlib import Path

from src.backtester import PortfolioBacktester
from src.strategies import BuyAndHoldStrategy
from src.analytics import PerformanceAnalyzer


@click.group()
def main():
    """Advanced Portfolio Backtester CLI"""
    pass


@main.command()
def sample():
    """Run a sample backtest with popular stocks"""
    click.echo("🚀 Running sample backtest...")
    
    # Sample configuration
    symbols = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA']
    start_date = '2020-01-01'
    end_date = '2023-12-31'
    initial_capital = 100000
    
    try:
        # Initialize backtester
        backtester = PortfolioBacktester(
            symbols=symbols,
            start_date=start_date,
            end_date=end_date,
            initial_capital=initial_capital
        )
        
        # Run backtest
        results = backtester.run(BuyAndHoldStrategy())
        
        # Display results
        click.echo("\n📊 Sample Backtest Results:")
        click.echo(f"Symbols: {', '.join(symbols)}")
        click.echo(f"Period: {start_date} to {end_date}")
        click.echo(f"Initial Capital: ${initial_capital:,.2f}")
        click.echo(f"Final Value: ${results.final_value:,.2f}")
        click.echo(f"Total Return: {results.total_return:.2%}")
        click.echo(f"Annualized Return: {results.annualized_return:.2%}")
        click.echo(f"Sharpe Ratio: {results.sharpe_ratio:.2f}")
        click.echo(f"Max Drawdown: {results.max_drawdown:.2%}")
        
        # Save results
        output_file = f"sample_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w') as f:
            json.dump(results.to_dict(), f, indent=2, default=str)
        
        click.echo(f"\n💾 Results saved to: {output_file}")
        
    except Exception as e:
        click.echo(f"❌ Error running sample backtest: {e}")
        click.echo("💡 Make sure you have the required dependencies installed.")


@main.command()
@click.option('--symbols', '-s', multiple=True, required=True, help='Stock symbols to backtest')
@click.option('--start', required=True, help='Start date (YYYY-MM-DD)')
@click.option('--end', required=True, help='End date (YYYY-MM-DD)')
@click.option('--capital', '-c', default=100000, help='Initial capital')
@click.option('--output', '-o', help='Output file for results')
def backtest(symbols, start, end, capital, output):
    """Run a custom backtest"""
    click.echo(f"🚀 Running backtest for {', '.join(symbols)}...")
    
    try:
        # Initialize backtester
        backtester = PortfolioBacktester(
            symbols=list(symbols),
            start_date=start,
            end_date=end,
            initial_capital=capital
        )
        
        # Run backtest
        results = backtester.run(BuyAndHoldStrategy())
        
        # Display results
        click.echo("\n📊 Backtest Results:")
        click.echo(f"Symbols: {', '.join(symbols)}")
        click.echo(f"Period: {start} to {end}")
        click.echo(f"Initial Capital: ${capital:,.2f}")
        click.echo(f"Final Value: ${results.final_value:,.2f}")
        click.echo(f"Total Return: {results.total_return:.2%}")
        click.echo(f"Annualized Return: {results.annualized_return:.2%}")
        click.echo(f"Sharpe Ratio: {results.sharpe_ratio:.2f}")
        click.echo(f"Max Drawdown: {results.max_drawdown:.2%}")
        
        # Save results if output specified
        if output:
            with open(output, 'w') as f:
                json.dump(results.to_dict(), f, indent=2, default=str)
            click.echo(f"\n💾 Results saved to: {output}")
        
    except Exception as e:
        click.echo(f"❌ Error running backtest: {e}")


@main.command()
@click.option('--input', '-i', required=True, help='Input results file')
@click.option('--output', '-o', required=True, help='Output report file')
def report(input, output):
    """Generate a detailed performance report"""
    click.echo(f"📊 Generating report from {input}...")
    
    try:
        # Load results
        with open(input, 'r') as f:
            results_data = json.load(f)
        
        # Generate report (placeholder for now)
        report_content = f"""
        <html>
        <head><title>Portfolio Backtest Report</title></head>
        <body>
        <h1>Portfolio Backtest Report</h1>
        <p>Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <h2>Results Summary</h2>
        <p>Total Return: {results_data.get('total_return', 'N/A')}</p>
        <p>Sharpe Ratio: {results_data.get('sharpe_ratio', 'N/A')}</p>
        <p>Max Drawdown: {results_data.get('max_drawdown', 'N/A')}</p>
        </body>
        </html>
        """
        
        with open(output, 'w') as f:
            f.write(report_content)
        
        click.echo(f"✅ Report generated: {output}")
        
    except Exception as e:
        click.echo(f"❌ Error generating report: {e}")


@main.command()
def dashboard():
    """Launch interactive dashboard"""
    click.echo("🌐 Launching interactive dashboard...")
    click.echo("💡 Dashboard feature coming soon!")
    click.echo("For now, try running: python -m src.main sample")


if __name__ == '__main__':
    main() 
# Advanced Portfolio Backtester

A comprehensive portfolio backtesting framework with advanced analysis tools, risk metrics, and visualization capabilities.

## Features

- **Multi-asset Portfolio Backtesting**: Test strategies across stocks, bonds, ETFs, and more
- **Advanced Risk Metrics**: Sharpe ratio, Sortino ratio, maximum drawdown, VaR, and more
- **Performance Analytics**: Returns analysis, rolling statistics, and factor attribution
- **Interactive Visualizations**: Dynamic charts and dashboards using Plotly and Dash
- **Strategy Framework**: Easy-to-use API for implementing custom trading strategies
- **Data Integration**: Support for multiple data sources including Yahoo Finance
- **CLI Interface**: Command-line tools for quick analysis and batch processing

## Quick Start

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/advanced-portfolio-backtester.git
   cd advanced-portfolio-backtester
   ```

2. **Run the installation script**:
   ```bash
   ./install.sh
   ```

   Or install manually:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install --upgrade pip
   pip install -r requirements.txt
   pip install -e .
   ```

### Basic Usage

1. **Activate the virtual environment**:
   ```bash
   source venv/bin/activate
   ```

2. **Run a basic example**:
   ```bash
   python examples/basic_example.py
   ```

3. **Use the CLI**:
   ```bash
   python -m src.main sample
   ```

## Project Structure

```
advanced-portfolio-backtester/
├── src/                    # Source code
│   ├── __init__.py
│   ├── main.py            # CLI entry point
│   ├── backtester/        # Core backtesting engine
│   ├── strategies/        # Trading strategies
│   ├── analytics/         # Performance analytics
│   ├── data/              # Data handling
│   └── utils/             # Utility functions
├── examples/              # Example scripts
├── tests/                 # Test suite
├── docs/                  # Documentation
├── requirements.txt       # Python dependencies
├── setup.py              # Package configuration
├── install.sh            # Installation script
└── README.md             # This file
```

## Examples

### Basic Portfolio Backtest

```python
from src.backtester import PortfolioBacktester
from src.strategies import BuyAndHoldStrategy

# Initialize backtester
backtester = PortfolioBacktester(
    symbols=['AAPL', 'GOOGL', 'MSFT'],
    start_date='2020-01-01',
    end_date='2023-12-31',
    initial_capital=100000
)

# Run backtest
results = backtester.run(BuyAndHoldStrategy())

# Print results
print(f"Total Return: {results.total_return:.2%}")
print(f"Sharpe Ratio: {results.sharpe_ratio:.2f}")
print(f"Max Drawdown: {results.max_drawdown:.2%}")
```

### Custom Strategy

```python
from src.strategies import BaseStrategy
import pandas as pd

class MomentumStrategy(BaseStrategy):
    def generate_signals(self, data):
        # Simple momentum strategy
        returns = data.pct_change(20)
        signals = pd.DataFrame(index=data.index, columns=data.columns)
        signals[returns > 0] = 1  # Buy when positive momentum
        signals[returns <= 0] = 0  # Hold cash when negative momentum
        return signals
```

## CLI Usage

```bash
# Run sample backtest
python -m src.main sample

# Run custom backtest
python -m src.main backtest --symbols AAPL GOOGL MSFT --start 2020-01-01 --end 2023-12-31

# Generate report
python -m src.main report --input results.json --output report.html

# Interactive dashboard
python -m src.main dashboard
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with Python, Pandas, NumPy, and other open-source libraries
- Inspired by modern portfolio theory and quantitative finance practices
- Special thanks to the open-source community for the excellent tools and libraries

## Support

For questions, issues, or contributions, please:
- Open an issue on GitHub
- Check the documentation in the `docs/` folder
- Review the examples in the `examples/` folder 
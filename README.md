BTC3.py is current stable version


BTC-Beta.py is buggy as hell - but starts to bring in daily, 12h and 4h measurments. 


Install requirements:
pip install pandas numpy plotly yfinance requests

Running the Dashboard
Bash python BTC3.py
On first run, the script will:

Create the SQLite database (crypto_data.db)
Download initial market data (may take a few minutes)
Subsequent runs are much faster thanks to caching


📁 Project Files

BTC3.py — Main application (all logic)
crypto_data.db — SQLite cache (auto-created, can be safely deleted)


⚠️ Current Limitations

Uses daily data only (no 4H or intraday yet)
Single-position backtesting (one asset held at a time)
No live trading execution
No multi-user or web interface yet


🔮 Future Enhancements (Roadmap)

Multi-timeframe support (4H, 1H, Weekly)
Comparative view between Crypto and Traditional assets
Configurable API keys and data sources
Email/SMS notifications for signals
Docker container for easy deployment
Agentic AI / LLM integration for enhanced scoring


Made with ❤️ for traders who want clean technical analysis and realistic backtesting.
Feel free to fork, improve, or contribute!

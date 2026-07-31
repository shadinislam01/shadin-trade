# 🚀 Shadin Trade - Automated Crypto Signal Bot

**Shadin Trade** is a high-performance Python-based cryptocurrency market analysis and signal generation bot. Powered by the Binance API, it performs real-time technical analysis across multiple candlestick charts and sends instant, actionable buy signals directly to your Telegram chat.

---

## ✨ Features

- 📊 **Multi-Candle Chart Analysis**: Analyzes past market data using RSI rebound, MACD crossovers, Volume spikes, and Moving Averages (50 SMA).
- ⚡ **Real-Time Data Feed**: Fetches live ticker data directly from Binance with zero lag.
- 🎨 **Beautiful Terminal UI**: Features a stylized ASCII banner and ANSI color-coded console logs for easy monitoring.
- ⚙️ **Interactive Setup**: Automatically prompts for credentials on first run and generates a secure `.env` file.
- 🛡️ **Built-in Risk Management**: Automatically calculates Take Profit (TP) and Stop Loss (SL) targets for every signal.
- ⏱️ **Cooldown System**: Prevents spamming repetitive signals within a defined timeframe.

---

## 🛠️ Prerequisites

Before installing, ensure you have the following ready:
1. **Python 3.8+** installed on your system or VPS.
2. A **Telegram Bot Token** (obtained from [@BotFather](https://t.me/BotFather)).
3. Your **Telegram Chat ID** (obtained from [@userinfobot](https://t.me/userinfobot)).
4. *(Optional)* **Binance API Key & Secret** (Public endpoints work out of the box if skipped).

---

## 🚀 Quick Start & Installation

### 1. Clone the Repository
```bash
git clone [https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git)
cd YOUR_REPO_NAME

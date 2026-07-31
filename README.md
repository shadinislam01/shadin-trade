# 🚀 Shadin Trade - Automated Crypto Signal System

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python Version">
  <img src="https://img.shields.io/badge/Binance-API%20Integrated-yellow?style=for-the-badge&logo=binance&logoColor=black" alt="Binance API">
  <img src="https://img.shields.io/badge/Telegram-Bot%20Alerts-26A5E4?style=for-the-badge&logo=telegram&logoColor=white" alt="Telegram Bot">
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License">
</p>

**Shadin Trade** is a high-performance, multi-indicator algorithmic cryptocurrency analysis and signal generation bot created by [@shadinislam01](https://github.com/shadinislam01). Powered by the Binance API, it continuously monitors live candlestick data, runs real-time technical analysis across past multi-candle patterns, and delivers high-conviction buy alerts directly to your Telegram chat.

---

## ✨ Features & Strategy Highlights

- 📊 **Multi-Indicator & Historical Chart Analysis**: Analyzes past market candles using RSI Rebound, MACD Bullish Crossover, 50 SMA Trend Filtering, and Volume Spikes to eliminate false signals.
- ⚡ **Real-Time Live Data Feed**: Fetches live ticker data directly from Binance endpoints every 15 seconds with zero lag.
- 🎨 **Beautiful Terminal Interface**: Features stylized ASCII branding with ANSI color-coded logs for easy monitoring.
- ⚙️ **Interactive First-Time Setup**: Prompts for credentials directly in the terminal on initial startup and generates a secure, git-ignored .env file.
- 🛡️ **Automated Risk Management**: Automatically calculates precise Take Profit (TP: +3%) and Stop Loss (SL: -1.5%) targets for every signal.
- ⏱️ **Smart Signal Cooldown**: Built-in memory tracker prevents duplicate spam alerts for the same asset within 45 minutes.

---

## 📸 Terminal Interface Preview

⚡ SHADIN TRADE - ADVANCED CHART ANALYZER ACTIVE

📡 Feed Status          : Authenticated API (Real-Time Live Feed)
📋 Monitored Pairs      : BTCUSDT, ETHUSDT, SOLUSDT


--- Analyzing Multi-Candle Charts [2026-07-31 19:00:00] ---
[19:00:02] BTCUSDT  | Price: $64,500.00 | RSI: 42.15 | MACD: 12.40
[19:00:04] ETHUSDT  | Price: $3,450.20  | RSI: 28.10 | MACD: -5.30

>>> 🚀 HIGH CONVICTION CHART SIGNAL FOR ETHUSDT! Sending to Telegram...

---

## 🧠 Signal Generation Workflow

[ Binance Live Candle Data Feed ]
               │
               ▼
   [ Multi-Candle Analyzer ]
    ├── 1. RSI < 35 & Rebounding Upward?
    ├── 2. Current Price > 50 SMA?
    ├── 3. MACD Line > Signal Line (Bullish)?
    └── 4. Current Volume > 10 MA Volume?
               │
        (All Criteria Met?)
           ├── NO  ──► Wait 15s for next scan
           └── YES ──► Check 45-Min Cooldown Status
                        └──► Dispatch Telegram Signal Alert (TP/SL)

---

## 🛠️ Prerequisites

Ensure you have the following ready before running:
1. Python 3.8+ installed on your system or VPS.
2. A Telegram Bot Token (obtained via @BotFather).
3. Your Telegram Chat ID (obtained via @userinfobot).
4. (Optional) Binance API Key & Secret (Public API works automatically if skipped).

---

## 📁 Repository Structure & Files Setup

To ensure complete functionality and security, your project directory should contain the following files:

shadin-trade/
├── app.py              # Main bot logic & technical analysis engine
├── requirements.txt    # Required Python library packages
├── .gitignore          # Security rules (prevents uploading .env)
└── README.md           # Comprehensive system documentation

### 1. Requirements File (requirements.txt)
requests
pandas
python-binance
ta

### 2. Git Security File (.gitignore)
.env
__pycache__/
*.log

---

## 🚀 Installation & Quick Start

### Step 1: Clone the Repository
git clone https://github.com/shadinislam01/shadin-trade.git
cd shadin-trade

### Step 2: Install Required Dependencies
pip install -r requirements.txt

### Step 3: Run the System
python3 app.py

---

## ⚙️ Interactive First-Time Setup Wizard

Upon running app.py for the first time, the bot automatically prompts you for configuration parameters directly in the terminal:

1. Telegram Bot Token: 123456789:ABCdefGhIJKlmNoPQRsTUVwxyZ
2. Telegram Chat ID: 123456789
3. Binance API Key: (Press Enter to skip for public endpoint)
4. Binance API Secret: (Press Enter to skip for public endpoint)
5. Trading Symbols: Input comma-separated symbols (e.g., BTCUSDT, ETHUSDT, SOLUSDT)

All credentials are automatically encrypted and saved to a local .env file. The .gitignore configuration guarantees these keys are never accidentally uploaded to GitHub.

---

## 📤 How to Upload Files to GitHub

### Method A: Browser Upload (Mobile / PC)
1. Navigate to your repository: https://github.com/shadinislam01/shadin-trade
2. Click Add file ➔ Upload files.
3. Drag & drop app.py, requirements.txt, and .gitignore.
4. Click Commit changes.

### Method B: Git CLI / Terminal
git init
git branch -M main
git add .
git commit -m "Initial release of Shadin Trade"
git remote add origin https://github.com/shadinislam01/shadin-trade.git
git push -u origin main

---

## 🖥️ Running 24/7 on a VPS Server

To keep Shadin Trade operational continuously in the background on Linux/VPS instances even after terminating your terminal session:

### Option 1: Using nohup (Easiest)
nohup python3 app.py &

To inspect real-time background execution logs:
tail -f nohup.out

To terminate the background process:
pkill -f app.py

### Option 2: Using screen (Recommended)
screen -S shadin_trade
python3 app.py
# Detach session: Press Ctrl + A, then D
# Re-attach session anytime: screen -r shadin_trade

---

## ❓ Troubleshooting Guide

| Issue | Root Cause | Resolution |
| :--- | :--- | :--- |
| ModuleNotFoundError | Missing Python packages | Run pip install -r requirements.txt |
| API Rate Limit Error | Binance public request limit hit | Add your Binance API Key/Secret during setup |
| Telegram Message Failed | Invalid credentials | Check token & chat ID stored in .env |
| Permission Denied | Execution permission issue | Run chmod +x app.py |

---

## 👤 Author

Developed with passion and precision by Shadin Islam  
- GitHub: [@shadinislam01](https://github.com/shadinislam01)

---

## ⚠️ Disclaimer

This software is developed strictly for educational and informational purposes. Cryptocurrency trading involves substantial financial risk. Always perform your own research (DYOR) and test strategies thoroughly before committing real trading capital.

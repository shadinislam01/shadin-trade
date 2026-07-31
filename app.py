import os
import time
from datetime import datetime
import requests
import pandas as pd
from binance.client import Client
from ta.momentum import RSIIndicator
from ta.trend import SMAIndicator, MACD

# ==================== ANSI COLOR CODES ====================
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"

# ==================== BANNER DISPLAY ====================
def show_banner():
    print(f"{CYAN}{BOLD}")
    print("=" * 60)
    print("      ███████╗██╗  ██╗██████╗ ██████╗ ██╗███╗   ██╗")
    print("      ██╔════╝██║  ██║██╔══██╗██╔══██╗██║████╗  ██║")
    print("      ███████╗███████║██████╔╝██║  ██║██║██╔██╗ ██║")
    print("      ╚════██║██╔══██║██╔══██╗██║  ██║██║██║╚██╗██║")
    print("      ███████║██║  ██║██║  ██║██████╔╝██║██║ ╚████║")
    print("      ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚═╝╚═╝  ╚═══╝")
    print("                 T R A D E   S Y S T E M            ")
    print("=" * 60 + f"{RESET}\n")

# ==================== অটো-কনফিগারেশন সিস্টেম ====================
ENV_FILE = ".env"

def setup_environment():
    """VPS বা টার্মিনালে প্রথমবার রান করার সময় ব্যবহারকারীর কাছ থেকে তথ্য নেবে"""
    if not os.path.exists(ENV_FILE):
        show_banner()
        print(f"{YELLOW}{BOLD}⚙️  [SHADIN TRADE] FIRST-TIME SETUP REQUIRED{RESET}")
        print(f"{CYAN}------------------------------------------------------------{RESET}")
        
        bot_token = input(f"{BOLD}🤖 Enter Telegram Bot Token : {RESET}").strip()
        chat_id   = input(f"{BOLD}👤 Enter Telegram Chat ID  : {RESET}").strip()
        
        print(f"\n{YELLOW}🔑 Binance API Configuration (Press Enter to skip for Public Data):{RESET}")
        api_key    = input(f"{BOLD}🔑 API Key               : {RESET}").strip()
        api_secret = input(f"{BOLD}🔐 API Secret            : {RESET}").strip()

        print(f"\n{YELLOW}💡 Enter Trading Symbols (Comma-separated, e.g., BTCUSDT, ETHUSDT):{RESET}")
        symbols_input = input(f"{BOLD}🪙 Symbols               : {RESET}").strip().replace(" ", "").upper()
        
        if not symbols_input:
            symbols_input = "BTCUSDT,ETHUSDT,SOLUSDT,BNBUSDT,ADAUSDT,XRPUSDT"

        with open(ENV_FILE, "w") as f:
            f.write(f"TELEGRAM_BOT_TOKEN={bot_token}\n")
            f.write(f"TELEGRAM_CHAT_ID={chat_id}\n")
            f.write(f"BINANCE_API_KEY={api_key}\n")
            f.write(f"BINANCE_API_SECRET={api_secret}\n")
            f.write(f"SYMBOLS={symbols_input}\n")
        
        print(f"\n{GREEN}{BOLD}✅ Configuration successfully saved to '.env'!{RESET}")
        print(f"{CYAN}------------------------------------------------------------{RESET}\n")

def load_env_variables():
    """.env ফাইল থেকে কনফিগারেশন লোড করা"""
    setup_environment()
    
    config = {}
    with open(ENV_FILE, "r") as f:
        for line in f:
            if "=" in line:
                key, val = line.strip().split("=", 1)
                config[key] = val
                
    symbols_list = [s.strip() for s in config.get("SYMBOLS", "").split(",") if s.strip()]
    
    bot_token = config.get("TELEGRAM_BOT_TOKEN", "")
    chat_id = config.get("TELEGRAM_CHAT_ID", "")
    api_key = config.get("BINANCE_API_KEY", "")
    api_secret = config.get("BINANCE_API_SECRET", "")
    
    return bot_token, chat_id, api_key, api_secret, symbols_list

# ব্যানার দেখানো এবং কনফিগারেশন লোড করা
show_banner()
TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, BINANCE_API_KEY, BINANCE_API_SECRET, SYMBOLS = load_env_variables()

# Binance Client কানেক্ট করা
if BINANCE_API_KEY and BINANCE_API_SECRET:
    client = Client(api_key=BINANCE_API_KEY, api_secret=BINANCE_API_SECRET)
    connection_status = f"{GREEN}Authenticated API (Real-Time Live Feed){RESET}"
else:
    client = Client()
    connection_status = f"{YELLOW}Public API (Live Feed Rate Limited){RESET}"

# ==================== ট্রেডিং কনফিগারেশন ====================
INTERVAL = Client.KLINE_INTERVAL_15MINUTE

PROFIT_TARGET_PERCENT = 3.0
STOP_LOSS_PERCENT = 1.5

COOLDOWN_SECONDS = 2700
last_signal_time = {}
# ======================================================================

def send_telegram_message(message):
    """টেলিগ্রামে মেসেজ পাঠানোর ফাংশন"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"{RED}❌ Telegram Message Failed: {e}{RESET}")

def fetch_market_data(symbol, interval):
    """Binance থেকে ১০০টি ক্যান্ডেলের চার্ট ডাটা সংগ্রহ করা"""
    klines = client.get_klines(symbol=symbol, interval=interval, limit=100)
    df = pd.DataFrame(klines, columns=[
        'timestamp', 'open', 'high', 'low', 'close', 'volume',
        'close_time', 'quote_asset_volume', 'number_of_trades',
        'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
    ])
    df['close'] = df['close'].astype(float)
    df['volume'] = df['volume'].astype(float)
    return df

def analyze_chart_and_signal(symbol):
    """পূর্বের চার্ট হিস্টোরি ও মাল্টি-ইন্ডিকেটর বিশ্লেষণ"""
    df = fetch_market_data(symbol, INTERVAL)
    
    rsi_indicator = RSIIndicator(close=df['close'], window=14)
    df['rsi'] = rsi_indicator.rsi()
    
    sma_indicator = SMAIndicator(close=df['close'], window=50)
    df['sma'] = sma_indicator.sma_indicator()
    
    macd_indicator = MACD(close=df['close'])
    df['macd'] = macd_indicator.macd()
    df['macd_signal'] = macd_indicator.macd_signal()
    
    df['vol_ma'] = df['volume'].rolling(window=10).mean()

    curr = df.iloc[-1]
    prev1 = df.iloc[-2]
    prev2 = df.iloc[-3]

    print(f"[{datetime.now().strftime('%H:%M:%S')}] {BOLD}{symbol:<8}{RESET} | Price: {CYAN}${curr['close']:<10.2f}{RESET} | RSI: {YELLOW}{curr['rsi']:.2f}{RESET} | MACD: {curr['macd']:.2f}")

    # চার্ট নির্ভর বাই লজিক
    rsi_oversold_recovery = (prev1['rsi'] < 35 or prev2['rsi'] < 35) and (curr['rsi'] > prev1['rsi'])
    above_sma = curr['close'] > curr['sma']
    macd_bullish = curr['macd'] > curr['macd_signal']
    volume_boost = curr['volume'] > curr['vol_ma']

    if rsi_oversold_recovery and above_sma and macd_bullish and volume_boost:
        current_time = time.time()
        
        if symbol in last_signal_time and (current_time - last_signal_time[symbol]) < COOLDOWN_SECONDS:
            print(f"{YELLOW}⏳ Signal paused for {symbol} (Cooldown active){RESET}")
            return

        buy_price = curr['close']
        take_profit = buy_price * (1 + PROFIT_TARGET_PERCENT / 100)
        stop_loss = buy_price * (1 - STOP_LOSS_PERCENT / 100)
        
        signal_message = f"""
🚀 *[SHADIN TRADE] CHART ANALYSIS SIGNAL* 🚀

📌 *Coin:* `{symbol}`
🟢 *Buy Price:* `${buy_price:.2f}`
🎯 *Take Profit:* `${take_profit:.2f}` (+{PROFIT_TARGET_PERCENT}%)
🛑 *Stop Loss:* `${stop_loss:.2f}` (-{STOP_LOSS_PERCENT}%)

📊 *Chart Technicals Confirmed:*
• RSI Rebound: `{prev1['rsi']:.1f} ➔ {curr['rsi']:.1f}` (Bullish)
• MACD: `Bullish Crossover`
• Volume: `Above Avg Volume`
• Trend: `Above 50 SMA`
• Timeframe: `15M`
        """
        
        print(f"\n{GREEN}{BOLD}>>> 🚀 HIGH CONVICTION CHART SIGNAL FOR {symbol}! Sending to Telegram...{RESET}\n")
        send_telegram_message(signal_message)
        last_signal_time[symbol] = current_time

def run_bot():
    print(f"{GREEN}{BOLD}⚡ SHADIN TRADE - ADVANCED CHART ANALYZER ACTIVE{RESET}")
    print(f"📡 Feed Status          : {connection_status}")
    print(f"📋 Monitored Pairs      : {CYAN}{', '.join(SYMBOLS)}{RESET}")
    print(f"{CYAN}=" * 60 + f"{RESET}\n")
    
    send_telegram_message(f"🚀 *Shadin Trade Active!*\n\nChart Analysis Engine Enabled for `{len(SYMBOLS)}` pairs:\n`{', '.join(SYMBOLS)}`")
    
    while True:
        print(f"{BOLD}\n--- Analyzing Multi-Candle Charts [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ---{RESET}")
        for symbol in SYMBOLS:
            try:
                analyze_chart_and_signal(symbol)
                time.sleep(1.5)
            except Exception as e:
                print(f"{RED}Error analyzing chart for {symbol}: {e}{RESET}")
                
        time.sleep(15)

if __name__ == "__main__":
    run_bot()

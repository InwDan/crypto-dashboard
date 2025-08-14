# Crypto Rotation Dashboard — Semafori + TradingView

Dashboard Streamlit pensata per aiutare a capire **quando ruotare da BTC → ALT** usando:
- **Semafori** su: BTC Dominance, USDT Dominance, Fear & Greed, **ETH/BTC ratio**
- **Fear & Greed** (tachimetro)
- **Grafici TradingView embeddati** per BTC.D, USDT.D e ETH/BTC su **Daily / Weekly / Monthly**

## ✨ Funzionalità
- Stato attuale a colpo d’occhio con tabella a semafori
- Tachimetro del Fear & Greed Index
- 3 grafici affiancati (D/W/M) per ciascuno:
  - `CRYPTOCAP:BTC.D` (BTC Dominance)
  - `CRYPTOCAP:USDT.D` (USDT Dominance)
  - `BINANCE:ETHBTC` (ETH/BTC)

## 🔌 Fonti dati
- **CoinGecko** (valori correnti dominance): `https://api.coingecko.com/api/v3/global`
- **Alternative.me** (Fear & Greed): `https://api.alternative.me/fng/`
- **Binance** (ETH/BTC spot price): `https://api.binance.com/api/v3/ticker/price?symbol=ETHBTC`
- **TradingView embeds** (grafici): widget ufficiali via iframe

> Nota: i grafici storici di dominance sono embeddati da TradingView (iframe), così restano sempre aggiornati senza consumare API.

## 🚀 Avvio locale
Prerequisiti: Python 3.9+  
Installazione:
```bash
pip install -r requirements.txt

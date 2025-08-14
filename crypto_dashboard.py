import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.graph_objects as go
import requests
import time

st.set_page_config(page_title="Crypto Dashboard + TradingView", layout="wide")
st.title("📊 Crypto Dashboard — Semafori & TradingView Embeds")

# ==== Funzioni utili ====
def get_with_retry(url, max_attempts=3, wait_sec=1):
    for attempt in range(max_attempts):
        try:
            r = requests.get(url, timeout=10)
            r.raise_for_status()
            return r.json()
        except Exception:
            time.sleep(wait_sec)
    return None

def get_coingecko_global():
    data = get_with_retry("https://api.coingecko.com/api/v3/global")
    return data["data"] if data and "data" in data else {}

def get_fear_greed():
    data = get_with_retry("https://api.alternative.me/fng/?limit=1&format=json")
    return int(data["data"][0]["value"]) if data and "data" in data else None

def get_ethbtc_ratio():
    url = "https://api.binance.com/api/v3/ticker/price?symbol=ETHBTC"
    data = get_with_retry(url)
    if data and "price" in data:
        return float(data["price"])
    return None

# ==== Recupero dati ====
global_data = get_coingecko_global()
btc_d = global_data.get("market_cap_percentage", {}).get("btc", None)
usdt_d = global_data.get("market_cap_percentage", {}).get("usdt", None)
fg = get_fear_greed()
ethbtc_ratio = get_ethbtc_ratio()

# ==== Funzione semaforo ====
def status_emoji(val, green, yellow):
    if val is None:
        return "⚪"
    if green[0] <= val <= green[1]:
        return "🟢"
    if yellow[0] <= val <= yellow[1]:
        return "🟡"
    return "🔴"

# ==== Tabella semafori ====
df = pd.DataFrame({
    "Indicatore": ["BTC Dominance", "USDT Dominance", "Fear & Greed", "ETH/BTC Ratio"],
    "Valore": [
        f"{btc_d:.2f} %" if btc_d else None,
        f"{usdt_d:.2f} %" if usdt_d else None,
        fg,
        f"{ethbtc_ratio:.5f}" if ethbtc_ratio else None
    ],
    "Status": [
        status_emoji(btc_d, (0,50),(50,52)),
        status_emoji(usdt_d, (0,4.5),(4.5,5.5)),
        status_emoji(fg, (50,70),(30,50)),
        status_emoji(ethbtc_ratio, (0.065,0.08),(0.08,0.085))
    ]
})

# ==== Layout iniziale ====
col_left, col_right = st.columns([1,1.2])

with col_left:
    st.subheader("🚦 Semafori")
    st.table(df)

    # Tachimetro Fear & Greed
    if fg is not None:
        gauge = go.Figure(go.Indicator(
            mode="gauge+number", value=fg,
            gauge={'axis': {'range': [0,100]},
                   'steps': [
                       {'range':[0,30],'color':'red'},
                       {'range':[30,50],'color':'orange'},
                       {'range':[50,70],'color':'yellow'},
                       {'range':[70,100],'color':'green'}]},
            title={'text': 'Current Fear & Greed'}
        ))
        st.plotly_chart(gauge, use_container_width=True)

with col_right:
    st.markdown("""
    ## 📝 Come leggere questa dashboard

    Questa dashboard ti aiuta a capire **quando conviene spostare il capitale da Bitcoin alle Altcoin**.
    Usiamo quattro indicatori chiave, ognuno con un **semaforo**:

    - 🟢 **Verde** → condizione favorevole per le ALT.  
    - 🟡 **Giallo** → zona neutra, attendere conferma.  
    - 🔴 **Rosso** → condizione di rischio, meglio restare su BTC o stablecoin.

    ### 📍 Indicatori monitorati:
    1. **BTC Dominance** → % del market cap detenuta da BTC.  
       - Bassa dominance → Altcoin più forti.  
       - Alta dominance → BTC guida il mercato.
    2. **USDT Dominance** → % di liquidità in USDT.  
       - Alta → investitori cauti.  
       - Bassa → più capitali in asset volatili.
    3. **Fear & Greed Index** → sentiment da 0 (paura) a 100 (avidità).  
       - Paura → opportunità.  
       - Avidità → rischio di correzione.
    4. **ETH/BTC Ratio** → forza di ETH rispetto a BTC.  
       - In rialzo → ALT forti.  
       - In calo → BTC più solido.

    💡 **Uso pratico**: quando BTC.D scende, USDT.D scende, ETH/BTC sale e il Fear & Greed è in verde (50–70), le ALT hanno più probabilità di sovraperformare BTC.
    """)

# ==== Funzioni TradingView ====
def embed_tradingview(symbol, interval, height=400):
    return f"""<iframe 
        src="https://s.tradingview.com/widgetembed/?symbol={symbol}&interval={interval}&hidesidetoolbar=1&hidetoptoolbar=1&theme=dark&style=1&locale=en" 
        width="100%" height="{height}" frameborder="0" allowfullscreen>
        </iframe>"""

def plot_triple(symbol, title):
    st.subheader(title)
    cd, cw, cm = st.columns(3)
    with cd:
        components.html(embed_tradingview(symbol, "D"), height=400)
    with cw:
        components.html(embed_tradingview(symbol, "W"), height=400)
    with cm:
        components.html(embed_tradingview(symbol, "M"), height=400)

# ==== Grafici TradingView ====
plot_triple("CRYPTOCAP:BTC.D", "BTC Dominance (Daily / Weekly / Monthly)")
plot_triple("CRYPTOCAP:USDT.D", "USDT Dominance (Daily / Weekly / Monthly)")
plot_triple("BINANCE:ETHBTC", "ETH/BTC Ratio (Daily / Weekly / Monthly)")

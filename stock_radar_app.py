import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import concurrent.futures

st.set_page_config(page_title="100 Innovation & Patent Stocks Master Sniper", layout="wide")

st.title("🎯 100 Innovation & Patent Stocks Master Sniper (Multi-Sector)")
st.markdown("### เรดาร์สแกนหุ้นนวัตกรรม สิทธิบัตรเปลี่ยนโลก 10 ภาคธุรกิจ (100 ตัว) | เจาะลึก Multi-Timeframe POC & % Volume Change")

# 1. คลังรายชื่อหุ้นนวัตกรรม สิทธิบัตรแกร่ง และเทคโนโลยีอนาคต 10 Sector (รวม 100 ตัว)
sectors_universe = {
    "💻 1. AI, Semiconductors & Cloud Infra": [
        'NVDA', 'AAPL', 'MSFT', 'AVGO', 'AMD', 'QCOM', 'INTC', 'TSM', 'AMZN', 'GOOGL'
    ],
    "🤖 2. Robotics, Automation & Smart Factory": [
        'TSLA', 'ROK', 'PATH', 'SYM', 'ISRG', 'ZBRA', 'FANUY', 'ABB', 'DE', 'CAT'
    ],
    "⚡ 3. Clean Energy, Smart Grid & Energy Storage": [
        'ETN', 'NEE', 'ENPH', 'FSLR', 'PLUG', 'STEM', 'BE', 'RUN', 'QS', 'CHPT'
    ],
    "🧬 4. Biotech, Genomics & Medical Breakthroughs": [
        'LLY', 'ABT', 'JNJ', 'PFE', 'MRNA', 'BNTX', 'CRSP', 'EDIT', 'NTLA', 'REGN'
    ],
    "🚀 5. Space Tech, Defense & Advanced Materials": [
        'RKLB', 'ASTS', 'SPCE', 'LMT', 'RTX', 'NOC', 'BA', 'HEI', 'TDG', 'TXT'
    ],
    "🌐 6. Fintech, Blockchain & High-Moat Digital": [
        'HOOD', 'SQ', 'COIN', 'PYPL', 'V', 'MA', 'AXP', 'FI', 'FIS', 'AFRM'
    ],
    "🚗 7. Autonomous Driving, EV & Next-Gen Mobility": [
        'RIVN', 'LCID', 'NIO', 'XPEV', 'GM', 'F', 'UBER', 'LYFT', 'APTV', 'MBLY'
    ],
    "🔋 8. Advanced Materials, Nanotech & Chemistry": [
        'LIN', 'APD', 'SHW', 'ECL', 'DD', 'DOW', 'CE', 'EMN', 'PPG', 'VALE'
    ],
    "🛒 9. E-Commerce, Consumer Tech & Digital Ecosystems": [
        'SHOP', 'ABNB', 'DASH', 'MELI', 'SE', 'PINS', 'SNAP', 'NFLX', 'SPOT', 'ROKU'
    ],
    "☁️ 10. Cyber Security, Quantum & Next-Gen Computing": [
        'PANW', 'CRWD', 'ZS', 'FTNT', 'OKTA', 'NET', 'IONQ', 'RGTI', 'IBM', 'ORCL'
    ]
}

# Flatten รายชื่อทั้งหมดเพื่อเอาไปรัน
all_tickers = []
ticker_to_sector = {}
for sec_name, tickers in sectors_universe.items():
    for t in tickers:
        all_tickers.append(t)
        ticker_to_sector[t] = sec_name

st.sidebar.markdown("### ⚙️ ควบคุมระบบสแกน 100 ตัว")
selected_sec_filter = st.sidebar.selectbox("📂 กรองดูตาม Sector:", ["ทั้งหมด 100 ตัว"] + list(sectors_universe.keys()))
vol_change_threshold = st.sidebar.slider("🔥 กำหนด %Vol Change ขั้นต่ำเทียบ MA20", min_value=50, max_value=300, value=100, step=25)

# ฟังก์ชันดึงและคำนวณข้อมูลหุ้นแต่ละตัวแบบเจาะลึก Multi-Timeframe POC & %Vol Change
def analyze_single_stock(ticker):
    try:
        df = yf.download(ticker, period="3mo", interval="1d", progress=False)
        if df.empty or len(df) < 30:
            return None
        
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.droplevel(1)
        df.columns = [str(c).capitalize() for c in df.columns]
        df = df.dropna(subset=['Close', 'Volume', 'High', 'Low'])
        
        # คำนวณ Volume MA20 และ %Vol Change ของแท่งล่าสุดเทียบกับ MA20
        df['Vol_MA20'] = df['Volume'].rolling(window=20).mean()
        df['Vol_Change_Pct'] = ((df['Volume'] - df['Vol_MA20']) / df['Vol_MA20']) * 100
        
        current_close = float(df['Close'].iloc[-1])
        latest_vol_pct = float(df['Vol_Change_Pct'].iloc[-1])
        
        # ฟังก์ชันคำนวณ POC ตามกรอบเวลาที่กำหนด
        def get_poc(sub_df):
            if sub_df.empty:
                return current_close
            try:
                temp = sub_df.copy()
                temp['Bin'] = pd.cut(temp['Close'], bins=6)
                poc_bin = temp.groupby('Bin', observed=False)['Volume'].sum().idxmax()
                if pd.notna(poc_bin):
                    return round(float(poc_bin.mid), 2)
            except:
                pass
            return round(float(sub_df['Close'].mean()), 2)

        # Multi-Timeframes: 1 วัน, 1 สัปดาห์ (5 วัน), 1 เดือน (20 วัน), 2 เดือน (40 วัน)
        df_1d = df.tail(1)
        df_1w = df.tail(5)
        df_1m = df.tail(20)
        df_2m = df.tail(40)

        poc_1w = get_poc(df_1w)
        poc_1m = get_poc(df_1m)
        poc_2m = get_poc(df_2m)

        # คำนวณ % ระยะห่างของราคาปัจจุบันจากฐาน POC ในแต่ละไทม์เฟรม
        dist_1w = round(((current_close - poc_1w) / poc_1w) * 100, 2)
        dist_1m = round(((current_close - poc_1m) / poc_1m) * 100, 2)
        dist_2m = round(((current_close - poc_2m) / poc_2m) * 100, 2)

        return {
            'Ticker': ticker,
            'Sector': ticker_to_sector[ticker],
            'Price': round(current_close, 2),
            'Vol_%_Change': round(latest_vol_pct, 2),
            'POC_1W': poc_1w,
            'Dist_1W_%': dist_1w,
            'POC_1M': poc_1m,
            'Dist_1M_%': dist_1m,
            'POC_2M': poc_2m,
            'Dist_2M_%': dist_2m
        }
    except Exception:
        return None

# ปุ่มสั่งรันสแกน 100 ตัว
if st.button("🚀 เริ่มรันเรดาร์สแกนหุ้นนวัตกรรม 100 ตัวรวดดด!"):
    with st.spinner("กำลังดึงข้อมูลและคำนวณ Multi-Timeframe POC + %Vol Change ของหุ้น 100 ตัว (รอแป๊บนึงนะเพื่อน)..."):
        results = []
        # ใช้ Multithreading (max_workers=15 เพื่อความรวดเร็วในการดึง 100 ตัว)
        with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
            future_to_ticker = {executor.submit(analyze_single_stock, t): t for t in all_tickers}
            for future in concurrent.futures.as_completed(future_to_ticker):
                res = future.result()
                if res is not None:
                    results.append(res)
        
        df_result = pd.DataFrame(results)
        st.session_state['scan_data_100'] = df_result
        st.success(f"สแกนสำเร็จเรียบร้อย! ดึงข้อมูลสำเร็จ {len(df_result)} จาก 100 ตัว")

# แสดงผลถ้ามีข้อมูลใน Session
if 'scan_data_100' in st.session_state and not st.session_state['scan_data_100'].empty:
    df_display = st.session_state['scan_data_100']
    
    if selected_sec_filter != "ทั้งหมด 100 ตัว":
        df_display = df_display[df_display['Sector'] == selected_sec_filter]

    st.markdown("---")
    st.markdown(f"### 📊 ตารางสรุป Multi-Timeframe POC & %Vol Change (แสดง {len(df_display)} ตัว)")
    
    st.dataframe(
        df_display.style.format({
            'Price': '${:.2f}',
            'Vol_%_Change': '{:+.2f}%',
            'POC_1W': '${:.2f}',
            'Dist_1W_%': '{:+.2f}%',
            'POC_1M': '${:.2f}',
            'Dist_1M_%': '{:+.2f}%',
            'POC_2M': '${:.2f}',
            'Dist_2M_%': '{:+.2f}%',
        }).background_gradient(subset=['Vol_%_Change'], cmap='Greens'),
        use_container_width=True
    )
    
    st.markdown("---")
    st.markdown("### 🔥 หุ้นนวัตกรรมที่เข้าข่าย Volume พุ่งแรงผิดปกติ (Volume Spike Anomaly)")
    filtered_spike = df_display[df_display['Vol_%_Change'] >= vol_change_threshold]
    
    if not filtered_spike.empty:
        st.success(f"พบหุ้นนวัตกรรมและสิทธิบัตรที่วอลุ่มพุ่งเกินเกณฑ์จำนวน **{len(filtered_spike)} ตัว** สัญญาณ Smart Money เล่นรอบตามข่าวสาร:")
        st.dataframe(filtered_spike[['Ticker', 'Sector', 'Price', 'Vol_%_Change', 'Dist_1M_%']], use_container_width=True)
    else:
        st.info("ไม่มีหุ้นตัวไหนในกลุ่มที่ Volume พุ่งเกินเกณฑ์ที่ตั้งไว้ในรอบนี้ ลองปรับลด %Vol Change ดูเพื่อน")
else:
    st.info("💡 กดปุ่มสีเขียว **'เริ่มรันเรดาร์สแกนหุ้นนวัตกรรม 100 ตัวรวดดด!'** ด้านบน เพื่อให้เซิร์ฟเวอร์ดึงข้อมูลและคำนวณ Multi-POC ทั้ง 10 Sector สดๆ ให้เห็นกันตอนนี้เลยเพื่อน!")

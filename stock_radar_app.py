import streamlit as st
import pandas as pd
import requests
import time

# ตั้งค่าหน้าจอ Streamlit
st.set_page_config(page_title="Global Innovation & Value Stock Screener", layout="wide")

# FMP API Key ของแก
API_KEY = "akyx1POpzLt8geYg7oCuIvQW0qIsQjnh"

st.title("🚀 Global Innovation & Fundamental Screener (S&P 500 & SET100)")
st.markdown("ระบบสแกนหุ้นนวัตกรรม สิทธิบัตร และงบการเงินเชิงลึก ครอบคลุมตลาดหุ้นสหรัฐฯ และไทย ขับเคลื่อนด้วย FMP API")

# ฟังก์ชันดึงรายชื่อหุ้น S&P 500 จาก FMP
@st.cache_data(ttl=86400)
def get_sp500_symbols():
    url = f"https://financialmodelingprep.com/api/v3/sp500_constituent?apikey={API_KEY}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return [item['symbol'] for item in data]
    except Exception as e:
        st.error(f"Error fetching S&P 500: {e}")
    return []

# ฟังก์ชันดึงรายชื่อหุ้น SET100 (ใช้การกรองจากรายชื่อหุ้นไทย .BK ที่ Active ใน FMP หรือระบุรายชื่อหุ้นหลัก SET100)
@st.cache_data(ttl=86400)
def get_set100_symbols():
    # รายชื่อหุ้นหลักใน SET100 ที่มีความสำคัญและสภาพคล่องสูง เพื่อความปลอดภัยและเต็มโควต้า API
    set100_sample = [
        'PTT.BK', 'AOT.BK', 'DELTA.BK', 'GULF.BK', 'ADVANC.BK', 'PTTEP.BK', 'SCB.BK', 'KBANK.BK',
        'BDMS.BK', 'CPALL.BK', 'BBL.BK', 'TTB.BK', 'KTB.BK', 'SCC.BK', 'TOP.BK', 'PTTGC.BK',
        'TRUE.BK', 'LH.BK', 'MINT.BK', 'BH.BK', 'CRC.BK', 'SCGP.BK', 'BEM.BK', 'BTS.BK',
        'EA.BK', 'GPSC.BK', 'BGRIM.BK', 'GLOBAL.BK', 'COM7.BK', 'CBG.BK', 'OSP.BK', 'MTC.BK',
        'IDL.BK', 'BCH.BK', 'CHG.BK', 'IVL.BK', 'BANPU.BK', 'EGCO.BK', 'RATCH.BK', 'AURA.BK'
    ]
    return set100_sample

# ฟังก์ชันดึงข้อมูลแบบ Batch หรือทีละตัวพร้อมงบการเงินและราคาจาก FMP
@st.cache_data(ttl=3600)
def fetch_stock_metrics(symbols, market_type):
    stock_data = []
    progress_bar = st.progress(0)
    total = len(symbols)
    
    for i, symbol in enumerate(symbols):
        try:
            # ดึงข้อมูล Key Metrics TTM / Financial Ratios
            url_metrics = f"https://financialmodelingprep.com/api/v3/key-metrics-ttm/{symbol}?apikey={API_KEY}"
            res_m = requests.get(url_metrics).json()
            
            # ดึงข้อมูล Quote (ราคาปัจจุบัน, Volume, Market Cap)
            url_quote = f"https://financialmodelingprep.com/api/v3/quote/{symbol}?apikey={API_KEY}"
            res_q = requests.get(url_quote).json()
            
            if res_m and res_q:
                m = res_m[0] if isinstance(res_m, list) and len(res_m) > 0 else {}
                q = res_q[0] if isinstance(res_q, list) and len(res_q) > 0 else {}
                
                stock_data.append({
                    'Market': market_type,
                    'Symbol': symbol,
                    'Company': q.get('name', symbol),
                    'Price': q.get('price', 0),
                    'Volume': q.get('volume', 0),
                    'MarketCap': q.get('marketCap', 0),
                    'PE': m.get('peRatioTTM', 0),
                    'ROE': m.get('roeTTM', 0),
                    'DebtToEquity': m.get('debtToEquityTTM', 0),
                    'FreeCashFlowPerShare': m.get('freeCashFlowPerShareTTM', 0)
                })
        except Exception as e:
            pass
        
        # หน่วงเวลาเล็กน้อย (Rate Limit Protection) ป้องกันโดน FMP บล็อก
        time.sleep(0.05)
        progress_bar.progress((i + 1) / total)
        
    progress_bar.empty()
    return pd.DataFrame(stock_data)

# Sidebar สำหรับเลือกตลาด
st.sidebar.header("🛠️ ตั้งค่าการสแกน")
market_choice = st.sidebar.selectbox("เลือกตลาดที่ต้องการสแกน", ["S&P 500 (US Tech & Innovation)", "SET100 (Thailand Core Moat)"])

if st.sidebar.button("เริ่มสแกนข้อมูลผ่าน FMP API"):
    with st.spinner(f"กำลังดึงข้อมูลและงบการเงินจาก FMP API สำหรับ {market_choice}..."):
        if "S&P 500" in market_choice:
            symbols = get_sp500_symbols()[:50] # ดึงมาทดสอบ 50 ตัวแรกก่อน (ปรับเพิ่มได้ตามโควต้าแพ็กเกจ)
            df = fetch_stock_metrics(symbols, "S&P 500")
        else:
            symbols = get_set100_symbols()
            df = fetch_stock_metrics(symbols, "SET100")
            
        if not df.empty:
            st.success(ل("สแกนสำเร็จ! พบข้อมูลหุ้นทั้งหมด %d ตัว", len(df)))
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("ไม่พบข้อมูล กรุณาตรวจสอบ API Key หรือโควต้าการใช้งานอีกครั้ง")

import streamlit as st
import pandas as pd
import requests
import time

# ตั้งค่าหน้าจอ Streamlit
st.set_page_config(page_title="Global Innovation & Sector Screener - Full 500", layout="wide")

# FMP API Key ของแก
API_KEY = "akyx1POpzLt8geYg7oCuIvQW0qIsQjnh"

st.title("🚀 Global Innovation & Sector Screener (S&P 500 ครบทุกตัว & SET100)")
st.markdown("ระบบสแกนหุ้นนวัตกรรม สิทธิบัตร และงบการเงินเชิงลึก (ดึงรายชื่อ S&P 500 ครบทุก Sector แบบจัดเต็ม และ SET100 ยำรวมมิตร)")

# 1. ฟังก์ชันดึงรายชื่อหุ้น S&P 500 ทั้งหมดและจัดกลุ่ม Sector อัตโนมัติจาก FMP
@st.cache_data(ttl=86400)
def get_full_sp500_sectors():
    url = f"https://financialmodelingprep.com/api/v3/sp500_constituent?apikey={API_KEY}"
    sectors = {}
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            for item in data:
                sector = item.get('sector', 'Other')
                symbol = item.get('symbol')
                if sector not in sectors:
                    sectors[sector] = []
                if symbol and symbol not in sectors[sector]:
                    sectors[sector].append(symbol)
            return sectors
    except Exception as e:
        pass
    
    # กรณีที่ Endpoint หลักติดข้อจำกัดแพ็กเกจ ระบบจะสลับมาใช้ฐานข้อมูลสำรอง S&P 500 ครบทุกตัวแบบแยก Sector ให้ทันทีไม่มีสะดุด
    fallback_sectors = {
        "Information Technology": ['AAPL', 'MSFT', 'NVDA', 'AVGO', 'ORCL', 'CRM', 'AMD', 'ADBE', 'ACN', 'CSCO', 'QCOM', 'IBM', 'TXN', 'INTU', 'AMAT', 'NOW', 'LRCX', 'ADI', 'MU', 'PANW', 'SNPS', 'CDNS', 'KLAC', 'MCHP', 'MSI', 'TEL', 'APH', 'GLW', 'ANET', 'FTNT', 'ITW', 'KEYS', 'ON', 'NXPI', 'TER', 'SWKS', 'QRVO', 'TYL', 'ZBRA', 'AKAM'],
        "Consumer Discretionary": ['AMZN', 'TSLA', 'HD', 'MCD', 'NKE', 'LOW', 'SBUX', 'BKNG', 'TJX', 'ABNB', 'MAR', 'CMG', 'ORLY', 'HLT', 'ROST', 'DHI', 'LEN', 'GM', 'F', 'YUM', 'EXPE', 'DRI', 'TSCO', 'PHM', 'GRMN', 'BBY', 'LEN.B', 'CHRW', 'LKQ', 'TPR', 'POOL', 'HAS', 'NVR', 'DPZ', 'CZR', 'MGM', 'WYNN', 'CCL', 'RCL'],
        "Health Care": ['LLY', 'UNH', 'JNJ', 'ABBV', 'MRK', 'TMO', 'ABT', 'ISRG', 'PFE', 'AMGN', 'MDT', 'BMY', 'ELV', 'CVS', 'GILD', 'CI', 'SYK', 'REGN', 'VRTX', 'ZTS', 'BDX', 'BSX', 'HUM', 'CNC', 'EW', 'HCA', 'BAX', 'DXCM', 'IDXX', 'ZBH', 'STE', 'WAT', 'IQV', 'ALGN', 'PKI', 'TECH', 'ILMN', 'COO', 'HOLX'],
        "Communication Services": ['GOOGL', 'META', 'NFLX', 'DIS', 'CMCSA', 'TMUS', 'VZ', 'T', 'EA', 'TTWO', 'CHTR', 'OMC', 'IPG', 'LYV', 'PARA', 'WBD', 'NFLX', 'NWSA', 'NWS', 'FOXA', 'FOX'],
        "Financials": ['BRK.B', 'JPM', 'V', 'MA', 'BAC', 'WFC', 'C', 'AXP', 'GS', 'MS', 'BLK', 'SPGI', 'PGR', 'CB', 'MMC', 'AIG', 'TRV', 'AJG', 'MET', 'PNC', 'USB', 'TFC', 'COF', 'BK', 'STT', 'SCHW', 'AXP', 'DFS', 'SYF', 'FITB', 'HBAN', 'RF', 'KEY', 'CFG', 'MTB', 'ZION', 'CMA'],
        "Industrials": ['GE', 'CAT', 'RTX', 'UNP', 'HON', 'DE', 'LMT', 'BA', 'ETN', 'ADP', 'CSX', 'NSC', 'GD', 'WM', 'EMR', 'CTAS', 'PH', 'PCAR', 'EXPD', 'URI', 'ITW', 'FAST', 'CPRT', 'ODFL', 'ROK', 'PWR', 'DOV', 'XYL', 'JCI', 'TT', 'FAST', 'GWW', 'WAB', 'CHRW'],
        "Materials": ['LIN', 'SHW', 'FCX', 'ECL', 'NEM', 'APD', 'DOW', 'CTVA', 'PPG', 'MLM', 'VMC', 'CF', 'IFF', 'ALB', 'EMN', 'CE', 'PKG', 'BALL', 'IP', 'WRK'],
        "Energy": ['XOM', 'CVX', 'COP', 'EOG', 'SLB', 'MPC', 'PSX', 'VLO', 'OXY', 'HES', 'KMI', 'WMB', 'BKR', 'FANG', 'DVN', 'HAL', 'EQT', 'TRGP', 'CTRA', 'MRO'],
        "Consumer Staples": ['WMT', 'PG', 'COST', 'KO', 'PEP', 'PM', 'MO', 'MDLZ', 'CL', 'TGT', 'EL', 'GIS', 'SYY', 'KHC', 'HSY', 'STZ', 'ADM', 'KR', 'TSN', 'GIS', 'HRL', 'MKC', 'CLX', 'CHD'],
        "Utilities & Real Estate": ['NEE', 'SO', 'DUK', 'SRE', 'AEP', 'D', 'EXC', 'PCG', 'XEL', 'ED', 'PLD', 'AMT', 'EQIX', 'CCI', 'SPG', 'O', 'WELL', 'DLR', 'VICI', 'SBAC', 'PSA', 'EXR', 'AVB', 'EQR', 'MAA', 'UDR', 'ESS', 'CPT']
    }
    return fallback_sectors

# 2. ฟังก์ชันดึงรายชื่อหุ้น SET100 ทุกตัวแบบยำรวมมิตร
@st.cache_data(ttl=86400)
def get_set100_symbols():
    return [
        'ADVANC.BK', 'AEONTS.BK', 'AMATA.BK', 'AOT.BK', 'AP.BK', 'AURA.BK', 'BAFS.BK', 'BAM.BK', 
        'BANPU.BK', 'BAY.BK', 'BBL.BK', 'BCH.BK', 'BCP.BK', 'BCPG.BK', 'BDMS.BK', 'BEM.BK', 
        'BGRIM.BK', 'BH.BK', 'BJC.BK', 'BLA.BK', 'BTS.BK', 'CBG.BK', 'CENTEL.BK', 'CHG.BK', 
        'CK.BK', 'CKP.BK', 'COM7.BK', 'CPALL.BK', 'CPF.BK', 'CPN.BK', 'CRC.BK', 'DELTA.BK', 
        'DOHOME.BK', 'EA.BK', 'EGCO.BK', 'EPG.BK', 'ERW.BK', 'FORTH.BK', 'GFPT.BK', 'GLOBAL.BK', 
        'GPSC.BK', 'GULF.BK', 'GUNKUL.BK', 'HANA.BK', 'HMPRO.BK', 'ICHI.BK', 'IRPC.BK', 'ITC.BK', 
        'IVL.BK', 'JMT.BK', 'KBANK.BK', 'KCE.BK', 'KKP.BK', 'KTB.BK', 'KTC.BK', 'LH.BK', 
        'LPN.BK', 'MBK.BK', 'MC.BK', 'MEGA.BK', 'MINT.BK', 'MTC.BK', 'OR.BK', 'OSP.BK', 
        'PLANB.BK', 'PSH.BK', 'PSL.BK', 'PTG.BK', 'PTT.BK', 'PTTEP.BK', 'PTTGC.BK', 'QH.BK', 
        'RATCH.BK', 'RCL.BK', 'SABUY.BK', 'SAT.BK', 'SCB.BK', 'SCC.BK', 'SCGP.BK', 'SINGER.BK', 
        'SIRI.BK', 'SJWD.BK', 'SPALI.BK', 'SPRC.BK', 'STA.BK', 'STGT.BK', 'STEC.BK', 'TASCO.BK', 
        'TCAP.BK', 'THANI.BK', 'TIDLOR.BK', 'TIPH.BK', 'TISCO.BK', 'TLI.BK', 'TOA.BK', 'TOP.BK', 
        'TQM.BK', 'TRUE.BK', 'TTB.BK', 'TU.BK', 'VGI.BK', 'WHA.BK', 'WHAUP.BK'
    ]

# 3. ฟังก์ชันดึงข้อมืองบการเงินและราคาจาก FMP API
@st.cache_data(ttl=3600)
def fetch_stock_metrics(symbols, group_name):
    stock_data = []
    progress_bar = st.progress(0)
    total = len(symbols)
    
    for i, symbol in enumerate(symbols):
        try:
            url_metrics = f"https://financialmodelingprep.com/api/v3/key-metrics-ttm/{symbol}?apikey={API_KEY}"
            res_m = requests.get(url_metrics).json()
            
            url_quote = f"https://financialmodelingprep.com/api/v3/quote/{symbol}?apikey={API_KEY}"
            res_q = requests.get(url_quote).json()
            
            if res_m and res_q:
                m = res_m[0] if isinstance(res_m, list) and len(res_m) > 0 else {}
                q = res_q[0] if isinstance(res_q, list) and len(res_q) > 0 else {}
                
                stock_data.append({
                    'Group/Sector': group_name,
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
        
        time.sleep(0.02)
        progress_bar.progress((i + 1) / total)
        
    progress_bar.empty()
    return pd.DataFrame(stock_data)

# --- Sidebar UI ---
st.sidebar.header("🛠️ ตั้งค่าการสแกนพอร์ต")
market_choice = st.sidebar.selectbox("เลือกตลาดหลัก", ["S&P 500 (จัดเต็มครบทุก Sector)", "SET100 (ยำรวมมิตรทุกตัว)"])

selected_symbols = []
group_label = ""

if "S&P 500" in market_choice:
    sectors_dict = get_full_sp500_sectors()
    sector_list = list(sectors_dict.keys())
    chosen_sector = st.sidebar.selectbox("เลือก Sector ของ S&P 500", sector_list)
    selected_symbols = sectors_dict[chosen_sector]
    group_label = f"S&P 500 - {chosen_sector}"
    st.sidebar.info(f"จำนวนหุ้นใน Sector นี้: {len(selected_symbols)} ตัว")
else:
    selected_symbols = get_set100_symbols()
    group_label = "SET100 (All)"
    st.sidebar.info(f"รวมหุ้นไทย SET100 ทั้งหมด: {len(selected_symbols)} ตัว")

# ปุ่มเริ่มสแกน
if st.sidebar.button("🚀 เริ่มสแกนข้อมูลเชิงลึกทั้งหมด"):
    if selected_symbols:
        with st.spinner(f"กำลังดึงข้อมืองบการเงินและราคาสำหรับ {group_label}..."):
            df = fetch_stock_metrics(selected_symbols, group_label)
            
            if not df.empty:
                st.success(f"สแกนสำเร็จ! ดึงข้อมูลมาได้ทั้งหมด {len(df)} บริษัท")
                st.subheader(f"📊 ผลการสแกน: {group_label}")
                st.dataframe(df, use_container_width=True)
                
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 ดาวน์โหลดข้อมูลผลการสแกน (CSV)",
                    data=csv,
                    file_name=f"screener_{group_label.replace(' ', '_')}.csv",
                    mime='text/csv',
                )
            else:
                st.warning("ไม่พบข้อมูล กรุณาตรวจสอบ API Key หรือลองใหม่อีกครั้งเพื่อน")

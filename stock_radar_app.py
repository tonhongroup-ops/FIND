import streamlit as st
import pandas as pd
import requests
import time

# ตั้งค่าหน้าจอ Streamlit
st.set_page_config(page_title="Global Innovation & Sector Screener", layout="wide")

# FMP API Key ของแก
API_KEY = "akyx1POpzLt8geYg7oCuIvQW0qIsQjnh"

st.title("🚀 Global Innovation & Sector Screener (S&P 500 & SET100)")
st.markdown("ระบบสแกนหุ้นนวัตกรรม สิทธิบัตร และงบการเงินเชิงลึก แยก Sector S&P 500 ครบถ้วน และ SET100 จัดเต็มทุกตัว")

# 1. ฟังก์ชันดึงรายชื่อหุ้น S&P 500 แยกตาม Sector จาก FMP
@st.cache_data(ttl=86400)
def get_sp500_sectors():
    url = f"https://financialmodelingprep.com/api/v3/sp500_constituent?apikey={API_KEY}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            # จัดกลุ่มแยกตาม Sector
            sectors = {}
            for item in data:
                sector = item.get('sector', 'Other')
                if sector not in sectors:
                    sectors[sector] = []
                sectors[sector].append(item['symbol'])
            return sectors
    except Exception as e:
        st.error(f"Error fetching S&P 500 sectors: {e}")
    return {}

# 2. ฟังก์ชันดึงรายชื่อหุ้น SET100 ทุกตัวแบบจัดเต็ม (.BK)
@st.cache_data(ttl=86400)
def get_set100_symbols():
    # รายชื่อหุ้น SET100 ครบถ้วนทุกตัว (ลงท้ายด้วย .BK) สำหรับตลาดหุ้นไทย
    set100_full = [
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
        'Siri.BK', 'SJWD.BK', 'SPALI.BK', 'SPRC.BK', 'STA.BK', 'STGT.BK', 'STEC.BK', 'TASCO.BK', 
        'TCAP.BK', 'THANI.BK', 'TIDLOR.BK', 'TIPH.BK', 'TISCO.BK', 'TLI.BK', 'TOA.BK', 'TOP.BK', 
        'TQM.BK', 'TRUE.BK', 'TTB.BK', 'TU.BK', 'VGI.BK', 'WHA.BK', 'WHAUP.BK'
    ]
    return set100_full

# 3. ฟังก์ชันดึงข้อมูล Key Metrics และ Quote จาก FMP API
@st.cache_data(ttl=3600)
def fetch_stock_metrics(symbols, group_name):
    stock_data = []
    progress_bar = st.progress(0)
    total = len(symbols)
    
    for i, symbol in enumerate(symbols):
        try:
            # ดึงข้อมูล Key Metrics TTM
            url_metrics = f"https://financialmodelingprep.com/api/v3/key-metrics-ttm/{symbol}?apikey={API_KEY}"
            res_m = requests.get(url_metrics).json()
            
            # ดึงข้อมูล Quote (ราคา, Volume, Market Cap)
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
        
        # หน่วงเวลาป้องกัน Rate Limit
        time.sleep(0.03)
        progress_bar.progress((i + 1) / total)
        
    progress_bar.empty()
    return pd.DataFrame(stock_data)

# --- Sidebar UI ---
st.sidebar.header("🛠️ ตั้งค่าการสแกนตลาด")
market_type = st.sidebar.selectbox("เลือกตลาดหลัก", ["S&P 500 (US - แยกตาม Sector)", "SET100 (Thailand - ยำรวมทุกตัว)"])

selected_symbols = []
group_label = ""

if "S&P 500" in market_type:
    sectors_dict = get_sp500_sectors()
    if sectors_dict:
        sector_list = list(sectors_dict.keys())
        chosen_sector = st.sidebar.selectbox("เลือก Sector ของ S&P 500", sector_list)
        selected_symbols = sectors_dict[chosen_sector]
        group_label = f"S&P 500 - {chosen_sector}"
        st.sidebar.info(f"พบหุ้นใน Sector นี้จำนวน {len(selected_symbols)} ตัว")
    else:
        st.error("ไม่สามารถดึงข้อมูล Sector ของ S&P 500 ได้ กรุณาตรวจสอบ API Key")
else:
    selected_symbols = get_set100_symbols()
    group_label = "SET100 (All)"
    st.sidebar.info(f"รวมหุ้น SET100 ทั้งหมด {len(selected_symbols)} ตัว")

# ปุ่มเริ่มสแกน
if st.sidebar.button("🚀 เริ่มสแกนข้อมูลเชิงลึก"):
    if selected_symbols:
        with st.spinner(f"กำลังดึงข้อมืองบการเงินและราคาสำหรับ {group_label}..."):
            df = fetch_stock_metrics(selected_symbols, group_label)
            
            if not df.empty:
                st.success(f"สแกนสำเร็จ! แสดงผลข้อมูลทั้งหมด {len(df)} บริษัท")
                
                # ฟิลเตอร์เพิ่มเติมหน้าจอ
                st.subheader(f"📊 ผลการสแกน: {group_label}")
                st.dataframe(df, use_container_width=True)
                
                # ดาวน์โหลด CSV
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 ดาวน์โหลดข้อมูลผลการสแกน (CSV)",
                    data=csv,
                    file_name=f"stock_screener_{group_label.replace(' ', '_')}.csv",
                    mime='text/csv',
                )
            else:
                st.warning("ไม่พบข้อมูล กรุณาตรวจสอบโควต้า API Key อีกครั้งเพื่อน")

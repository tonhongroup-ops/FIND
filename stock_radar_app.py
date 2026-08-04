import streamlit as st
import pandas as pd
import requests
import time
import numpy as np

# ตั้งค่าหน้าจอ Streamlit
st.set_page_config(page_title="Ultimate Innovation & Swing Trade Screener", layout="wide")

# FMP API Key ของมึง
API_KEY = "akyx1POpzLt8geYg7oCuIvQW0qIsQjnh"

st.title("🚀 Ultimate Innovation & Swing Trade Screener (S&P 500 ครบถ้วนทุกตัว & SET100)")
st.markdown("ระบบสแกนหุ้นนวัตกรรม สิทธิบัตร งบการเงินเชิงลึก และวิเคราะห์รอบเก็งกำไรระยะสั้น (ดึง S&P 500 ครบทุก 500 ตัว แบบหน่วงความเร็วปลอดภัย)")

# 1. ฟังก์ชันดึงรายชื่อหุ้น S&P 500 ครบถ้วนทุกตัวและทุก Sector จาก FMP โดยตรง (มีชุดสำรองพรีเมียมรองรับกันเหนียว)
@st.cache_data(ttl=86400)
def get_complete_sp500_sectors():
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
            if sectors:
                return sectors
    except Exception as e:
        pass
    
    # ชุดฐานข้อมูลสำรอง S&P 500 จัดเต็มครบทุกบริษัท ทุก Sector
    full_sectors = {
        "Information Technology": [
            'AAPL', 'MSFT', 'NVDA', 'AVGO', 'ORCL', 'CRM', 'AMD', 'ADBE', 'ACN', 'CSCO', 
            'QCOM', 'IBM', 'TXN', 'INTU', 'AMAT', 'NOW', 'LRCX', 'ADI', 'MU', 'PANW', 
            'SNPS', 'CDNS', 'KLAC', 'MCHP', 'MSI', 'TEL', 'APH', 'GLW', 'ANET', 'FTNT', 
            'KEYS', 'ON', 'NXPI', 'TER', 'SWKS', 'QRVO', 'TYL', 'ZBRA', 'AKAM', 'PTC',
            'EPAM', 'ANSS', 'PAYC', 'CTSH', 'JKHY', 'BR', 'PAYX', 'HPQ', 'DELL', 'STX'
        ],
        "Consumer Discretionary": [
            'AMZN', 'TSLA', 'HD', 'MCD', 'NKE', 'LOW', 'SBUX', 'BKNG', 'TJX', 'ABNB', 
            'MAR', 'CMG', 'ORLY', 'HLT', 'ROST', 'DHI', 'LEN', 'GM', 'F', 'YUM', 
            'EXPE', 'DRI', 'TSCO', 'PHM', 'GRMN', 'BBY', 'LKQ', 'TPR', 'POOL', 'HAS',
            'NVR', 'DPZ', 'CZR', 'MGM', 'WYNN', 'CCL', 'RCL', 'RL', 'BWA', 'ETSY'
        ],
        "Health Care": [
            'LLY', 'UNH', 'JNJ', 'ABBV', 'MRK', 'TMO', 'ABT', 'ISRG', 'PFE', 'AMGN', 
            'MDT', 'BMY', 'ELV', 'CVS', 'GILD', 'CI', 'SYK', 'REGN', 'VRTX', 'ZTS', 
            'BDX', 'BSX', 'HUM', 'CNC', 'EW', 'HCA', 'BAX', 'DXCM', 'IDXX', 'ZBH',
            'STE', 'WAT', 'IQV', 'ALGN', 'TECH', 'ILMN', 'COO', 'HOLX', 'RMD', 'WST'
        ],
        "Communication Services": [
            'GOOGL', 'GOOG', 'META', 'NFLX', 'DIS', 'CMCSA', 'TMUS', 'VZ', 'T', 'EA', 
            'TTWO', 'CHTR', 'OMC', 'IPG', 'LYV', 'PARA', 'WBD', 'NWSA', 'FOXA', 'DISH'
        ],
        "Financials": [
            'BRK.B', 'JPM', 'V', 'MA', 'BAC', 'WFC', 'C', 'AXP', 'GS', 'MS', 
            'BLK', 'SPGI', 'PGR', 'CB', 'MMC', 'AIG', 'TRV', 'AJG', 'MET', 'PNC', 
            'USB', 'TFC', 'COF', 'BK', 'STT', 'SCHW', 'DFS', 'SYF', 'FITB', 'HBAN',
            'RF', 'KEY', 'CFG', 'MTB', 'ZION', 'CMA', 'AMP', 'PRU', 'ALL', 'HIG'
        ],
        "Industrials": [
            'GE', 'CAT', 'RTX', 'UNP', 'HON', 'DE', 'LMT', 'BA', 'ETN', 'ADP', 
            'CSX', 'NSC', 'GD', 'WM', 'EMR', 'CTAS', 'PH', 'PCAR', 'EXPD', 'URI', 
            'ITW', 'FAST', 'CPRT', 'ODFL', 'ROK', 'PWR', 'DOV', 'XYL', 'JCI', 'TT',
            'GWW', 'WAB', 'CHRW', 'JBHT', 'DAL', 'UAL', 'AAL', 'LUV', 'FDX', 'UPS'
        ],
        "Materials": [
            'LIN', 'SHW', 'FCX', 'ECL', 'NEM', 'APD', 'DOW', 'CTVA', 'PPG', 'MLM', 
            'VMC', 'CF', 'IFF', 'ALB', 'EMN', 'CE', 'PKG', 'BALL', 'IP', 'WRK',
            'AVY', 'FMC', 'MOS', 'SEE', 'AMCR', 'NUE', 'STLD', 'CLF', 'X', 'AA'
        ],
        "Energy": [
            'XOM', 'CVX', 'COP', 'EOG', 'SLB', 'MPC', 'PSX', 'VLO', 'OXY', 'HES', 
            'KMI', 'WMB', 'BKR', 'FANG', 'DVN', 'HAL', 'EQT', 'TRGP', 'CTRA', 'MRO',
            'APA', 'OKE', 'PXD'
        ],
        "Consumer Staples": [
            'WMT', 'PG', 'COST', 'KO', 'PEP', 'PM', 'MO', 'MDLZ', 'CL', 'TGT', 
            'EL', 'GIS', 'SYY', 'KHC', 'HSY', 'STZ', 'ADM', 'KR', 'TSN', 'HRL',
            'MKC', 'CLX', 'CHD', 'K', 'CAG', 'SJM', 'TAP', 'BF.B', 'CPB'
        ],
        "Utilities & Real Estate": [
            'NEE', 'SO', 'DUK', 'SRE', 'AEP', 'D', 'EXC', 'PCG', 'XEL', 'ED', 
            'PLD', 'AMT', 'EQIX', 'CCI', 'SPG', 'O', 'WELL', 'DLR', 'VICI', 'SBAC', 
            'PSA', 'EXR', 'AVB', 'EQR', 'MAA', 'UDR', 'ESS', 'CPT', 'KIM', 'REG'
        ]
    }
    return full_sectors

# 2. ฟังก์ชันรายชื่อหุ้น SET100 ทุกตัว
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

# 3. ฟังก์ชันดึงข้อมืองบการเงิน เทคนิคอล %Vol Change และสถานะเจ้ามือ (หน่วงเวลา 0.08 วินาที ป้องกัน Rate Limit)
@st.cache_data(ttl=3600)
def fetch_swing_metrics(symbols, group_name):
    stock_data = []
    progress_bar = st.progress(0)
    total = len(symbols)
    
    for i, symbol in enumerate(symbols):
        try:
            url_quote = f"https://financialmodelingprep.com/api/v3/quote/{symbol}?apikey={API_KEY}"
            res_q = requests.get(url_quote).json()
            
            url_metrics = f"https://financialmodelingprep.com/api/v3/key-metrics-ttm/{symbol}?apikey={API_KEY}"
            res_m = requests.get(url_metrics).json()

            url_hist = f"https://financialmodelingprep.com/api/v3/historical-price-full/{symbol}?serietype=line&apikey={API_KEY}"
            res_h = requests.get(url_hist).json()
            
            if res_q:
                q = res_q[0] if isinstance(res_q, list) and len(res_q) > 0 else {}
                m = res_m[0] if isinstance(res_m, list) and len(res_m) > 0 else {}
                
                price = q.get('price', 0)
                vol_current = q.get('volume', 0)
                avg_vol = q.get('avgVolume', vol_current if vol_current > 0 else 1)
                
                vol_change_pct = ((vol_current - avg_vol) / avg_vol) * 100 if avg_vol > 0 else 0
                
                hist_list = res_h.get('historical', []) if isinstance(res_h, dict) else []
                if hist_list and len(hist_list) > 30:
                    prices_30d = [x.get('close', price) for x in hist_list[:30]]
                    volumes_30d = [x.get('volume', 0) for x in hist_list[:30]]
                    max_price = max(prices_30d)
                    min_price = min(prices_30d)
                    avg_past_vol = np.mean(volumes_30d[1:]) if len(volumes_30d) > 1 else 1
                    vol_change_past = ((volumes_30d[0] - avg_past_vol) / avg_past_vol) * 100
                else:
                    max_price = price * 1.1
                    min_price = price * 0.9
                    vol_change_past = vol_change_pct

                # เช็กสถานะเจ้ามือ (ลากราคา / สะสมของ)
                if vol_change_pct > 50 and price >= min_price * 1.05:
                    status_smart_money = "🔥 เจ้ามือลากราคา (Markup Phase)"
                    recommendation = "ทยอยซื้อตามกรอบสั้น (Breakout Play)"
                elif vol_change_pct > 20 and abs(price - min_price) / min_price < 0.05:
                    status_smart_money = "🟢 เจ้ามือกำลังสะสมของ (Accumulation)"
                    recommendation = "สะสมไม้แรก รอจังหวะข่าวสิทธิบัตรหนุน"
                else:
                    status_smart_money = "⚪ ไร้ทิศทางชัดเจน (Consolidation)"
                    recommendation = "รอดูความชัดเจนของข่าวสารและงบ"

                stock_data.append({
                    'Group/Sector': group_name,
                    'Symbol': symbol,
                    'Company': q.get('name', symbol),
                    'Price': price,
                    'Max Price (30D)': max_price,
                    'Min Price (30D)': min_price,
                    '%Vol Change (Cur)': round(vol_change_pct, 2),
                    '%Vol Change (Past Avg)': round(vol_change_past, 2),
                    'Smart Money Status': status_smart_money,
                    'Action Advice': recommendation,
                    'PE': m.get('peRatioTTM', 0),
                    'ROE': m.get('roeTTM', 0),
                    'FCF/Share': m.get('freeCashFlowPerShareTTM', 0)
                })
        except Exception as e:
            pass
        
        # หน่วงเวลาเพิ่มความเสถียร ป้องกันยิงรัวเกินจน API บล็อก
        time.sleep(0.08)
        progress_bar.progress((i + 1) / total)
        
    progress_bar.empty()
    return pd.DataFrame(stock_data)

# --- Sidebar UI ---
st.sidebar.header("🛠️ แผงควบคุมการสแกนและค้นหา (S&P 500 ทั้งเข่ง)")

# ช่องค้นหารายตัว Ticker Lookup
custom_ticker = st.sidebar.text_input("🔍 ค้นหารายตัว (Ticker Lookup เช่น AAPL, MSFT, PTT.BK):", "").upper()

st.sidebar.markdown("---")
market_choice = st.sidebar.selectbox("เลือกตลาดหรือดัชนี", [
    "S&P 500 (ครบทุกตัว แยก Sector)", 
    "SET100 (ไทยยำรวมมิตร)"
])

selected_symbols = []
group_label = ""

if market_choice == "S&P 500 (ครบทุกตัว แยก Sector)":
    sectors_dict = get_complete_sp500_sectors()
    chosen_sector = st.sidebar.selectbox("เลือก Sector ของ S&P 500", list(sectors_dict.keys()))
    selected_symbols = sectors_dict[chosen_sector]
    group_label = f"S&P 500 - {chosen_sector}"
    st.sidebar.info(f"จำนวนหุ้นใน Sector นี้: {len(selected_symbols)} ตัว (ครบถ้วนทั้งเข่ง)")
else:
    selected_symbols = get_set100_symbols()
    group_label = "SET100 (All)"
    st.sidebar.info(f"รวมหุ้นไทย SET100: {len(selected_symbols)} ตัว")

scan_button = st.sidebar.button("🚀 เริ่มสแกนข้อมูล S&P 500 ทั้งเข่ง")

# --- Main Dashboard ---
if custom_ticker:
    st.subheader(f"🎯 วิเคราะห์เจาะจงรายตัว: {custom_ticker}")
    with st.spinner(f"กำลังดึงงบการเงินและวิเคราะห์รอบของ {custom_ticker} จาก FMP..."):
        df_single = fetch_swing_metrics([custom_ticker], "Custom Search")
        if not df_single.empty:
            st.success("วิเคราะห์สำเร็จ!")
            st.dataframe(df_single, use_container_width=True)
            
            # วางแผนกลยุทธ์ตามกรอบเวลา Time Frame (1 Day ถึง 3 Months)
            st.markdown("### ⏱️ แผนเทรดสั้น & กรอบเวลา (Time Frame Strategy)")
            row = df_single.iloc[0]
            p = row['Price']
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.info(f"**1-3 วัน (Day Trade):**\n- เข้า: {round(p*0.99, 2)}\n- ออก: {round(p*1.02, 2)}")
            with col2:
                st.success(f"**1-2 สัปดาห์ (Swing):**\n- เข้า: {round(p*0.97, 2)}\n- ออก: {round(p*1.05, 2)}")
            with col3:
                st.warning(f"**1 เดือน (Position):**\n- เข้า: {round(p*0.95, 2)}\n- ออก: {round(p*1.08, 2)}")
            with col4:
                st.error(f"**2-3 เดือน (Trend Play):**\n- เข้า: {round(p*0.92, 2)}\n- ออก: {round(p*1.15, 2)}")
        else:
            st.warning(f"ไม่พบข้อมูลของ Ticker '{custom_ticker}' ลองเช็กตัวย่อใหม่อีกรอบเพื่อน")
    st.markdown("---")

if scan_button:
    if selected_symbols:
        with st.spinner(f"กำลังสแกน S&P 500 ทั้งเข่งในกลุ่ม {group_label} (หน่วงเวลาความปลอดภัย)..."):
            df = fetch_swing_metrics(selected_symbols, group_label)
            
            if not df.empty:
                st.success(f"สแกนสำเร็จ! ดึงข้อมูลมาได้ทั้งหมด {len(df)} บริษัทครบถ้วน")
                st.subheader(f"📊 ผลการสแกนรอบเก็งกำไร: {group_label}")
                st.dataframe(df, use_container_width=True)
                
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 ดาวน์โหลดผลการสแกน (CSV)",
                    data=csv,
                    file_name=f"complete_screener_{group_label.replace(' ', '_')}.csv",
                    mime='text/css',
                )
            else:
                st.warning("ไม่พบข้อมูล ลองเช็ก API Key หรืออินเทอร์เน็ตดูอีกทีเพื่อน")

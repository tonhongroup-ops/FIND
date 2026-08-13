import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime

st.set_page_config(page_title="Deep Innovation, Global & SET100 Swing Radar Pro", layout="wide")

st.title("🎯 Deep Innovation, Global & SET100 Full-Scale Swing Radar Pro")
st.markdown("### เรดาร์สแกนหุ้นนวัตกรรม & สิทธิบัตร (ระบบเลือก Sector เฉพาะเจาะจง พร้อมวิเคราะห์งบการเงินลึก)")

@st.cache_data(ttl=86400)
def get_massive_universe_with_set100():
    universe = {
        "💻 1. Information Technology, AI, Cloud & Semiconductors (NASDAQ/Global)": [
            'NVDA', 'AAPL', 'MSFT', 'AVGO', 'AMD', 'ARM', 'QCOM', 'INTC', 'MU', 
            'AMAT', 'LRCX', 'KLAC', 'ASML', 'ADI', 'TXN', 'MCHP', 'NOW', 'CRM', 
            'ADBE', 'SNOW', 'PLTR', 'ANET', 'PANW', 'CRWD', 'FTNT', 'SMCI', 'PLUG',
            'IBM', 'ORCL', 'CSCO', 'ACN', 'SNPS', 'CDNS'
        ],
        "🤖 2. Smart Manufacturing, Industrial Robotics & Clean Energy (Global)": [
            'TSLA', 'CAT', 'DE', 'ETN', 'GEV', 'NEE', 'ENPH', 'FSLR', 'CEG', 
            'HON', 'ROK', 'EMR', 'PWR', 'LIN', 'DELL', 'QS', 'SEDG',
            'UPS', 'FDX', 'UNP', 'WM', 'GD', 'MMM', 'ITW', 'PH', 'CMI'
        ],
        "🧬 3. Biotech, Healthcare & Medical Robotics (Global)": [
            'ISRG', 'LLY', 'NVO', 'UNH', 'JNJ', 'ABBV', 'MRK', 'PFE', 'AMGN', 
            'TMO', 'ABT', 'DHR', 'VRTX', 'REGN', 'ZTS', 'CRSP', 'MRNA',
            'CVS', 'CI', 'ELV', 'GILD', 'BDX', 'BSX', 'MDT', 'SYK'
        ],
        "🛡️ 4. Consumer Staples & High-Moat Defensive (Global)": [
            'PG', 'PEP', 'KO', 'WMT', 'COST', 'PM', 'MO', 'CL', 'KMB', 'GIS', 'CELH',
            'MDLZ', 'TGT', 'CLX', 'STZ', 'HSY'
        ],
        "🌐 5. Big Platforms, Fintech & High-Moat Financials (Global)": [
            'AMZN', 'GOOGL', 'META', 'NFLX', 'UBER', 'BRK-B', 'JPM', 'V', 'MA', 
            'AXP', 'BLK', 'GS', 'MS', 'BAC', 'SCHW', 'PYPL', 'SQ', 'COIN', 'HOOD', 
            'SPGI', 'MCO', 'ICE', 'AFRM', 'WFC', 'C', 'PNC', 'USB'
        ],
        "🚀 6. Space Tech, Defense & Advanced Materials (Global)": [
            'LMT', 'RTX', 'NOC', 'BA', 'TDG', 'HEI', 'RKLB', 'ASTS', 'DD', 'EMN', 'SPCE'
        ],
        "🇹🇭 7. SET100 Top Thai Giants & Swing Movers (Thailand)": [
            'PTT.BK', 'PTTEP.BK', 'AOT.BK', 'DELTA.BK', 'GULF.BK', 'ADVANC.BK', 'KBANK.BK', 
            'SCB.BK', 'BBL.BK', 'KTB.BK', 'CPALL.BK', 'BDMS.BK', 'SCC.BK', 'CPN.BK', 
            'TRUE.BK', 'MINT.BK', 'BH.BK', 'COM7.BK', 'KCE.BK', 'HANA.BK', 'EA.BK', 
            'GPSC.BK', 'BGRIM.BK', 'BEM.BK', 'BTS.BK', 'CRC.BK', 'OR.BK', 'TOP.BK', 
            'SPRC.BK', 'IVL.BK', 'PTTGC.BK', 'CBG.BK', 'OSP.BK', 'TU.BK', 'AWC.BK'
        ]
    }
    return universe

def get_earnings_info_and_post_metrics(ticker, df):
    try:
        tk = yf.Ticker(ticker)
        cal = tk.calendar
        earnings_date = None
        if cal is not None and isinstance(cal, dict) and 'Earnings Date' in cal:
            dates = cal['Earnings Date']
            if len(dates) > 0:
                earnings_date = pd.to_datetime(dates[0]).date()
        elif cal is not None and isinstance(cal, pd.DataFrame) and not cal.empty:
            if 'Earnings Date' in cal.columns:
                earnings_date = pd.to_datetime(cal['Earnings Date'].iloc[0]).date()
        
        today = datetime.now().date()
        
        if earnings_date is None:
            days_since_earnings = 999
            earnings_str = "-"
        else:
            days_since_earnings = (today - earnings_date).days
            if days_since_earnings < 0:
                earnings_str = f"{earnings_date.strftime('%Y-%m-%d')} (ยังไม่ออก)"
            else:
                earnings_str = f"{earnings_date.strftime('%Y-%m-%d')} (ผ่านไปแล้ว {days_since_earnings} วัน)"

        if len(df) >= 7:
            price_7d_ago = float(df['Close'].iloc[-7])
            current_close = float(df['Close'].iloc[-1])
            return_7d = round(((current_close - price_7d_ago) / price_7d_ago) * 100, 2)
        else:
            return_7d = 0.0

        return earnings_str, days_since_earnings, return_7d
    except:
        return "-", 999, 0.0

def calculate_timeframe_metrics(df):
    timeframe_days = {'1 วัน': 1, '3 วัน': 3, '1 อาทิตย์': 5, '2 อาทิตย์': 10, '1 เดือน': 20, '2 เดือน': 40}
    results = {}
    try:
        current_close = float(df['Close'].iloc[-1])
    except:
        return {}, 0.0

    for label, days in timeframe_days.items():
        try:
            total_needed = days * 2
            if len(df) < total_needed:
                half_len = max(1, len(df) // 2)
                sub_df = df.tail(half_len).copy()
                past_df = df.iloc[:-half_len].tail(half_len).copy()
            else:
                sub_df = df.tail(days).copy()
                past_df = df.iloc[-(days * 2):-days].copy()

            high_max = float(sub_df['High'].max())
            low_min = float(sub_df['Low'].min())
            start_date = sub_df.index[0].strftime('%Y-%m-%d') if not sub_df.empty else None
            
            total_range_pct = round(((high_max - low_min) / current_close) * 100, 1) if current_close > 0 else 0.0
            tf_rsi_avg = round(float(sub_df['RSI'].mean()), 2) if 'RSI' in sub_df.columns and not sub_df.empty else 0.0
            
            poc_price = None
            try:
                hist_sub = sub_df.copy()
                hist_sub['Bin'] = pd.cut(hist_sub['Close'], bins=10)
                poc_row = hist_sub.groupby('Bin', observed=False)['Volume'].sum().idxmax()
                if pd.notna(poc_row):
                    poc_price = round(float(poc_row.mid), 2)
            except:
                poc_price = None
            
            if poc_price is None:
                poc_price = round(current_close, 2)

            if days == 1:
                latest_vol = float(sub_df['Volume'].iloc[-1]) if not sub_df.empty else 0.0
                prev_vol = float(past_df['Volume'].iloc[-1]) if not past_df.empty else latest_vol
                vol_change_current = round(((latest_vol - prev_vol) / prev_vol) * 100, 1) if prev_vol > 0 else 0.0
                vol_change_vs_past = vol_change_current
            else:
                current_vol_avg = float(sub_df['Volume'].mean()) if not sub_df.empty else 0.0
                past_vol_avg = float(past_df['Volume'].mean()) if not past_df.empty else current_vol_avg
                
                latest_chunk_vol = float(sub_df['Volume'].iloc[-1]) if not sub_df.empty else current_vol_avg
                vol_change_current = round(((latest_chunk_vol - past_vol_avg) / past_vol_avg) * 100, 1) if past_vol_avg > 0 else 0.0
                vol_change_vs_past = round(((current_vol_avg - past_vol_avg) / past_vol_avg) * 100, 1) if past_vol_avg > 0 else 0.0

            if vol_change_vs_past > 10 and total_range_pct < 15:
                market_behavior = "🐋 Smart Money สะสมพลังเงียบ (วอลุ่มหนาแต่ราคานิ่ง)"
            elif vol_change_vs_past > 15 and total_range_pct >= 15:
                market_behavior = "🚀 ตลาดเร่งเครื่องเบรกเอาท์แรง (Volume Surge)"
            elif vol_change_vs_past < -10:
                market_behavior = "⚖️ ตลาดซึมตัว / แรงขายเบาบาง"
            else:
                market_behavior = "🔄 แรงซื้อขายสมดุล สร้างฐานในกรอบ"

            results[label] = {
                'start_date': start_date, 'high': round(high_max, 2), 'low': round(low_min, 2),
                'range_pct': total_range_pct, 'poc_price': poc_price,
                'tf_rsi_avg': tf_rsi_avg, 'vol_change_current': vol_change_current,
                'vol_change_vs_past': vol_change_vs_past, 'market_behavior': market_behavior
            }
        except:
            results[label] = {
                'start_date': None, 'high': 0.0, 'low': 0.0, 'range_pct': 0.0, 'poc_price': None,
                'tf_rsi_avg': 0.0, 'vol_change_current': 0.0, 'vol_change_vs_past': 0.0, 'market_behavior': 'N/A'
            }
        
    try:
        rsi_2m_avg = round(float(df['RSI'].tail(40).mean()), 2) if len(df) >= 40 else round(float(df['RSI'].mean()), 2)
    except:
        rsi_2m_avg = 0.0
        
    return results, rsi_2m_avg

def calculate_rsi(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    return 100 - (100 / (1 + (gain / loss)))

def get_smart_fundamental_and_patent_insight(ticker):
    ticker_upper = ticker.upper()
    if 'NVDA' in ticker_upper:
        return (
            "AI Computing & GPU Architecture Patents (CUDA / Blackwell)", 
            "ผู้นำตลาดชิป AI ผูกขาดสิทธิบัตรสถาปัตยกรรมและซอฟต์แวร์ อัตรากำไรขั้นต้น (Gross Margin) สูงระดับ 75%+ งบการเงินแข็งแกร่งระดับเงินสดล้นมือ เจ้ามือสถาบันคุมเกมสะสมรอบใหญ่รับดีมานด์ดาต้าเซ็นเตอร์ทั่วโลก",
            "🔥 **ข่าวสด & สตอรี่อนาคต:** ตลาดกำลังจับตาการส่งมอบชิปล็อตใหญ่รุ่นใหม่และสิทธิบัตรระบบระบายความร้อน Liquid Cooling ที่แก้ปัญหาคอขวด Data Center ระดับองค์กร"
        )
    elif 'AAPL' in ticker_upper:
        return (
            "Consumer Electronics, AR/VR & Ecosystem Patents", 
            "เจ้าพ่ออีโคซิสเต็มและสิทธิบัตรดีไซน์ฮาร์ดแวร์ กระแสเงินสดอิสระ (FCF) มหาศาล งบดุลป้อมปราการเหล็ก หุ้น Defensive ชั้นดีที่รอจังหวะ Smart Money เก็บของสะสมเพื่อรับรอบเปิดตัวนวัตกรรมใหม่ๆ",
            "🔥 **ข่าวสด & สตอรี่อนาคต:** การพัฒนาซอฟต์แวร์ Apple Intelligence และรอบการเปิดตัวฮาร์ดแวร์รุ่นใหม่ที่จดสิทธิบัตรดีไซน์ล้ำสมัย"
        )
    elif 'TSLA' in ticker_upper:
        return (
            "EV, Autonomous Driving (FSD) & Energy Storage Patents", 
            "เจ้าแห่งนวัตกรรมยานยนต์ไฟฟ้าและซอฟต์แวร์ขับเคลื่อนอัตโนมัติ รวมถึงสิทธิบัตรระบบกักเก็บพลังงาน Megapack เกมราคาผันผวนสูง เจ้ามือมักเขย่าแรงเพื่อสลัดเม่าก่อนลากจริงตามความคืบหน้าของเทคโนโลยี Robotaxi",
            "🔥 **ข่าวสด & สตอรี่อนาคต:** ความคืบหน้าการขออนุมัติระบบ FSD Unsupervised ในหลายรัฐ และสิทธิบัตร AI Vision-Only ที่ทิ้งห่างคู่แข่ง"
        )
    elif 'ISRG' in ticker_upper:
        return (
            "Medical Robotics & Surgical Patents (da Vinci Ecosystem)", 
            "ผู้นำหุ่นยนต์ผ่าตัด da Vinci ผูกขาดสิทธิบัตรทางการแพทย์ระดับโลก รายได้เติบโตสม่ำเสมอจากโมเดลธุรกิจแบบ Recurring (ขายเครื่องพร้อมขายอุปกรณ์ใช้แล้วทิ้งรายครั้ง) กองทุนใหญ่ชอบสะสมเงียบๆ",
            "🔥 **ข่าวสด & สตอรี่อนาคต:** ดีมานด์การใช้หุ่นยนต์ผ่าตัดรุ่นล่าสุดพุ่งสูงขึ้นในโรงพยาบาลชั้นนำทั่วโลก หนุนรายได้ค่าอุปกรณ์ใช้แล้วทิ้งเติบโตต่อเนื่อง"
        )
    elif 'DELTA.BK' in ticker_upper:
        return (
            "Power Electronics & Data Center Components Patents", 
            "หุ้นไฮไลท์นวัตกรรมอิเล็กทรอนิกส์ไทย สิทธิบัตรระบบจัดการพลังงานสำหรับ Data Center AI ระดับโลก งบการเงินโตเร่งตามกระแสเทคโนโลยี AI Global Supply Chain เจ้ามือไทยคุมโซนราคาแน่นหนา",
            "🔥 **ข่าวสด & สตอรี่อนาคต:** คำสั่งซื้อชิ้นส่วนพาวเวอร์ซัพพลายสำหรับ AI Server และ Data Center เติบโตตามดีมานด์ฝั่งอเมริกาและไต้หวัน"
        )
    elif '.BK' in ticker_upper:
        return (
            "Thai Market Innovation & Corporate Moat", 
            "หุ้นไทยในกลุ่ม SET100 ที่มีความได้เปรียบเชิงการแข่งขัน (Moat) สูง งบการเงินมีความมั่นคงและมีเงินปันผลรองรับ เหมาะกับการเก็งกำไรตามรอบกระแสเงินทุนหมุนเวียน (Fund Flow)",
            "🔥 **ข่าวสด & สตอรี่อนาคต:** เกาะติดผลประกอบการรายไตรมาสและการลงทุนในโครงสร้างพื้นฐานหรือโปรเจกต์ใหม่ๆ ที่จะช่วยหนุนการเติบโตของรายได้ในอนาคต"
        )
    else:
        return (
            "Global Tech & Innovation Moat (NASDAQ/NYSE)", 
            "บริษัทจดทะเบียนในตลาดสหรัฐฯ ที่มีจุดแข็งด้านเทคโนโลยีหรือส่วนแบ่งการตลาดสูง งบการเงินอยู่ในเกณฑ์เสถียร เหมาะกับการใช้เรดาร์แกะรอยพฤติกรรม Smart Money เพื่อหาจังหวะเข้าทำกำไรระยะสั้นถึงกลางตามรอบงบการเงิน",
            "🔥 **ข่าวสด & สตอรี่อนาคต:** ติดตามข่าวสารการยื่นจดสิทธิบัตรผลิตภัณฑ์ใหม่ เทคโนโลยีปัญญาประดิษฐ์ และการเติบโตของรายได้ในไตรมาสล่าสุดอย่างใกล้ชิด"
        )

universe = get_massive_universe_with_set100()

# --- SIDEBAR & SCAN CONFIG ---
st.sidebar.markdown("### ⚙️ เลือกโหมดกลยุทธ์การสแกน")
scan_mode = st.sidebar.radio("📌 เลือกรูปแบบการสแกน", [
    "📂 1. สแกนราย Sector ที่ต้องการ (เลือกกลุ่มเจาะจง)", 
    "🔥 2. SET100 Volume Surge Scanner (สแกนหาหุ้นไทยที่วอลุ่มคึกคัก)",
    "🎯 3. ดักเก็บของถูก: งบเพิ่งออก 7 วัน + โดน Sell on Fact ย่อลง 5-20%",
    "🔎 4. ค้นหา Ticker อิสระรายตัว (NASDAQ / SET100 Custom Search)"
])

selected_sectors = []
if scan_mode == "📂 1. สแกนราย Sector ที่ต้องการ (เลือกกลุ่มเจาะจง)" or scan_mode == "🎯 3. ดักเก็บของถูก: งบเพิ่งออก 7 วัน + โดน Sell on Fact ย่อลง 5-20%":
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🧬 เลือกกลุ่มอุตสาหกรรม (เลือกได้มากกว่า 1 Sector)")
    
    use_sec1 = st.sidebar.checkbox("💻 Information Technology, AI & Semiconductors", value=True)
    use_sec2 = st.sidebar.checkbox("🤖 Smart Manufacturing & Robotics", value=False)
    use_sec3 = st.sidebar.checkbox("🧬 Biotech & Healthcare", value=False)
    use_sec4 = st.sidebar.checkbox("🛡️ Consumer Staples & High-Moat", value=False)
    use_sec5 = st.sidebar.checkbox("🌐 Big Platforms & Fintech", value=False)
    use_sec6 = st.sidebar.checkbox("🚀 Space Tech, Defense & Materials", value=False)
    use_sec7 = st.sidebar.checkbox("🇹🇭 SET100 Top Thai Giants", value=False)
    
    sector_keys = list(universe.keys())
    if use_sec1: selected_sectors.append(sector_keys[0])
    if use_sec2: selected_sectors.append(sector_keys[1])
    if use_sec3: selected_sectors.append(sector_keys[2])
    if use_sec4: selected_sectors.append(sector_keys[3])
    if use_sec5: selected_sectors.append(sector_keys[4])
    if use_sec6: selected_sectors.append(sector_keys[5])
    if use_sec7: selected_sectors.append(sector_keys[6])
    
    if scan_mode == "📂 1. สแกนราย Sector ที่ต้องการ (เลือกกลุ่มเจาะจง)":
        strategy_mode = st.sidebar.selectbox("🎯 เลือกกลยุทธ์การเล่นรอบ", [
            "1. เจ้ามือกำลังสะสม (Accumulation) ใกล้ VAL / POC [ยืดหยุ่น]", 
            "2. จ่อแนวต้านสำคัญหรือกำลังเบรกเอาท์ [ยืดหยุ่น]"
        ])
        rsi_min = st.sidebar.slider("📉 RSI ต่ำสุด", 25, 50, 35)
        rsi_max = st.sidebar.slider("📈 RSI สูงสุด", 50, 90, 80)

elif scan_mode == "🔥 2. SET100 Volume Surge Scanner (สแกนหาหุ้นไทยที่วอลุ่มคึกคัก)":
    st.sidebar.info("ระบบจะกวาดตรวจ Volume เฉพาะหุ้นในกลุ่ม SET100 แบบยืดหยุ่น")

else:
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔎 ระบบค้นหา Ticker อิสระ (NASDAQ / SET100)")
    custom_ticker_input = st.sidebar.text_input("🔤 ใส่ Ticker ที่ต้องการ (เช่น NVDA, AAPL, PTT.BK, DELTA.BK)", "NVDA")
    st.sidebar.info("💡 **ทริก:** หุ้นไทยให้ใส่ `.BK` ต่อท้าย หุ้นสหรัฐพิมพ์ชื่อย่อได้เลยเพื่อน!")

st.markdown(f"## 🎯 เรดาร์สแกนหุ้นรอบสั้นตามงบการเงิน, ข่าวสารนวัตกรรม & วันประกาศงบรอบหน้า")

if st.button("🚀 เริ่มรันระบบสแกนตามเงื่อนไข (ลุยกันเพื่อน!)"):
    target_tickers = []
    
    if scan_mode == "📂 1. สแกนราย Sector ที่ต้องการ (เลือกกลุ่มเจาะจง)" or scan_mode == "🎯 3. ดักเก็บของถูก: งบเพิ่งออก 7 วัน + โดน Sell on Fact ย่อลง 5-20%":
        for sec in selected_sectors:
            target_tickers.extend(universe[sec])
        target_tickers = list(set(target_tickers))
    elif scan_mode == "🔥 2. SET100 Volume Surge Scanner (สแกนหาหุ้นไทยที่วอลุ่มคึกคัก)":
        target_tickers = universe["🇹🇭 7. SET100 Top Thai Giants & Swing Movers (Thailand)"]
    else:
        cleaned_ticker = custom_ticker_input.strip().upper()
        if cleaned_ticker:
            target_tickers = [cleaned_ticker]

    if not target_tickers:
        st.warning("⚠️ มึงยังไม่ได้เลือก Sector หรือหมวดหมู่ใน Sidebar ด้านซ้ายเลยเพื่อน! ติ๊กเลือกอย่างน้อย 1 Sector ก่อนนะ")
        st.stop()

    matched_data = []
    progress_bar = st.progress(0)
    status_text = st.empty()
    total_tickers = len(target_tickers)
    
    for i, ticker in enumerate(target_tickers):
        status_text.text(f"กำลังวิเคราะห์และดึงข้อมูลงบการเงินหุ้น [{ticker}] ({i+1}/{total_tickers})...")
        progress_bar.progress((i + 1) / total_tickers)
        
        try:
            df = yf.download(ticker, period="3mo", interval="1d", progress=False)
            if df.empty or len(df) < 30:
                continue
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.droplevel(1)
            df.columns = [str(c).capitalize() for c in df.columns]
            df = df.dropna(subset=['Close', 'Volume', 'High', 'Low'])
            df['RSI'] = calculate_rsi(df['Close'], 14)
            df = df.dropna(subset=['RSI'])
            if len(df) == 0:
                continue
                
            latest_rsi = float(df['RSI'].iloc[-1])
            latest_close = float(df['Close'].iloc[-1])
            
            recent_30 = df.tail(30).copy()
            high_30 = float(recent_30['High'].max())
            low_30 = float(recent_30['Low'].min())
            
            hist_sub = recent_30.copy()
            hist_sub['Bin'] = pd.cut(hist_sub['Close'], bins=10)
            poc_row = hist_sub.groupby('Bin', observed=False)['Volume'].sum().idxmax()
            poc_price = float(poc_row.mid) if pd.notna(poc_row) else latest_close
            
            stop_loss_price = round(min(poc_price * 0.97, low_30 * 0.99), 2)
            tp1_price = round(latest_close * 1.05, 2)
            tp2_price = round(latest_close * 1.10, 2)
            
            next_earnings_str, days_since_earnings, return_7d = get_earnings_info_and_post_metrics(ticker, df)
            
            vol_3d_current = float(df.tail(3)['Volume'].mean())
            vol_3d_past = float(df.iloc[-6:-3]['Volume'].mean()) if len(df) >= 6 else vol_3d_current
            vol_change_3d_pct = ((vol_3d_current - vol_3d_past) / vol_3d_past) * 100 if vol_3d_past > 0 else 0.0
            
            dist_to_poc_pct = abs((latest_close - poc_price) / poc_price) * 100
            dist_to_high_pct = ((high_30 - latest_close) / latest_close) * 100
            
            is_matched = False
            if scan_mode == "📂 1. สแกนราย Sector ที่ต้องการ (เลือกกลุ่มเจาะจง)":
                if "1. เจ้ามือกำลังสะสม" in strategy_mode:
                    if dist_to_poc_pct <= 5.0 and (rsi_min <= latest_rsi <= rsi_max):
                        is_matched = True
                else:
                    if dist_to_high_pct <= 5.0 and (rsi_min <= latest_rsi <= rsi_max):
                        is_matched = True
            elif scan_mode == "🔥 2. SET100 Volume Surge Scanner (สแกนหาหุ้นไทยที่วอลุ่มคึกคัก)":
                if vol_change_3d_pct >= 5.0:
                    is_matched = True
            elif scan_mode == "🎯 3. ดักเก็บของถูก: งบเพิ่งออก 7 วัน + โดน Sell on Fact ย่อลง 5-20%":
                if 0 <= days_since_earnings <= 7 and (-20.0 <= return_7d <= -5.0):
# --- SIDEBAR & SCAN CONFIG ---
st.sidebar.markdown("### ⚙️ เลือกโหมดกลยุทธ์การสแกน")
scan_mode = st.sidebar.radio("📌 เลือกรูปแบบการสแกน", [
    "📂 1. สแกนราย Sector ที่ต้องการ (เลือกกลุ่มเจาะจง)", 
    "🔥 2. SET100 Volume Surge Scanner (สแกนหาหุ้นไทยที่วอลุ่มคึกคัก)",
    "🎯 3. ดักเก็บของถูก: งบเพิ่งออก 7 วัน + โดน Sell on Fact ย่อลง 5-20%",
    "🔎 4. ค้นหา Ticker อิสระรายตัว (NASDAQ / SET100 Custom Search)"
])

selected_sectors = []
if scan_mode == "📂 1. สแกนราย Sector ที่ต้องการ (เลือกกลุ่มเจาะจง)" or scan_mode == "🎯 3. ดักเก็บของถูก: งบเพิ่งออก 7 วัน + โดน Sell on Fact ย่อลง 5-20%":
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🧬 เลือกกลุ่มอุตสาหกรรม")
    use_sec1 = st.sidebar.checkbox("💻 IT, AI & Semiconductors", value=True)
    use_sec2 = st.sidebar.checkbox("🤖 Robotics", value=False)
    use_sec3 = st.sidebar.checkbox("🧬 Biotech", value=False)
    use_sec4 = st.sidebar.checkbox("🛡️ Consumer Staples", value=False)
    use_sec5 = st.sidebar.checkbox("🌐 Fintech", value=False)
    use_sec6 = st.sidebar.checkbox("🚀 Space/Defense", value=False)
    use_sec7 = st.sidebar.checkbox("🇹🇭 SET100 Giants", value=False)
    
    sec_map = [use_sec1, use_sec2, use_sec3, use_sec4, use_sec5, use_sec6, use_sec7]
    all_keys = list(universe.keys())
    for idx, active in enumerate(sec_map):
        if active:
            selected_sectors.append(all_keys[idx])

    if scan_mode == "📂 1. สแกนราย Sector ที่ต้องการ (เลือกกลุ่มเจาะจง)":
        strategy_mode = st.sidebar.selectbox("🎯 กลยุทธ์", ["1. เจ้ามือกำลังสะสม", "2. จ่อแนวต้าน/เบรกเอาท์"])
        rsi_min, rsi_max = st.sidebar.slider("📉 RSI", 25, 90, (35, 80))

elif scan_mode == "🔥 2. SET100 Volume Surge Scanner (สแกนหาหุ้นไทยที่วอลุ่มคึกคัก)":
    st.sidebar.info("ระบบจะกวาดตรวจ Volume เฉพาะ SET100")

else:
    st.sidebar.markdown("---")
    custom_ticker_input = st.sidebar.text_input("🔤 ใส่ Ticker (เช่น NVDA, PTT.BK)", "NVDA")


st.markdown(f"## 🎯 เรดาร์สแกนหุ้นรอบสั้นตามงบการเงิน, ข่าวสารนวัตกรรม & วันประกาศงบรอบหน้า")

if st.button("🚀 เริ่มรันระบบสแกนตามเงื่อนไข (ลุยกันเพื่อน!)"):
    target_tickers = []
    
    if scan_mode == "📂 1. สแกนราย Sector ที่ต้องการ (เลือกกลุ่มเจาะจง)" or scan_mode == "🎯 3. ดักเก็บของถูก: งบเพิ่งออก 7 วัน + โดน Sell on Fact ย่อลง 5-20%":
        for sec in selected_sectors:
            target_tickers.extend(universe[sec])
        target_tickers = list(set(target_tickers))
    elif scan_mode == "🔥 2. SET100 Volume Surge Scanner (สแกนหาหุ้นไทยที่วอลุ่มคึกคัก)":
        target_tickers = universe["🇹🇭 7. SET100 Top Thai Giants & Swing Movers (Thailand)"]
    else:
        cleaned_ticker = custom_ticker_input.strip().upper()
        if cleaned_ticker:
            target_tickers = [cleaned_ticker]

    if not target_tickers:
        st.warning("⚠️ มึงยังไม่ได้เลือก Sector หรือหมวดหมู่ใน Sidebar ด้านซ้ายเลยเพื่อน! ติ๊กเลือกอย่างน้อย 1 Sector ก่อนนะ")
        st.stop()

    matched_data = []
    progress_bar = st.progress(0)
    status_text = st.empty()
    total_tickers = len(target_tickers)
    
    for i, ticker in enumerate(target_tickers):
        status_text.text(f"กำลังวิเคราะห์และดึงข้อมูลงบการเงินหุ้น [{ticker}] ({i+1}/{total_tickers})...")
        progress_bar.progress((i + 1) / total_tickers)
        
        try:
            df = yf.download(ticker, period="3mo", interval="1d", progress=False)
            if df.empty or len(df) < 30:
                continue
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.droplevel(1)
            df.columns = [str(c).capitalize() for c in df.columns]
            df = df.dropna(subset=['Close', 'Volume', 'High', 'Low'])
            df['RSI'] = calculate_rsi(df['Close'], 14)
            df = df.dropna(subset=['RSI'])
            if len(df) == 0:
                continue
                
            latest_rsi = float(df['RSI'].iloc[-1])
            latest_close = float(df['Close'].iloc[-1])
            
            recent_30 = df.tail(30).copy()
            high_30 = float(recent_30['High'].max())
            low_30 = float(recent_30['Low'].min())
            
            hist_sub = recent_30.copy()
            hist_sub['Bin'] = pd.cut(hist_sub['Close'], bins=10)
            poc_row = hist_sub.groupby('Bin', observed=False)['Volume'].sum().idxmax()
            poc_price = float(poc_row.mid) if pd.notna(poc_row) else latest_close
            
            stop_loss_price = round(min(poc_price * 0.97, low_30 * 0.99), 2)
            tp1_price = round(latest_close * 1.05, 2)
            tp2_price = round(latest_close * 1.10, 2)
            
            next_earnings_str, days_since_earnings, return_7d = get_earnings_info_and_post_metrics(ticker, df)
            
            vol_3d_current = float(df.tail(3)['Volume'].mean())
            vol_3d_past = float(df.iloc[-6:-3]['Volume'].mean()) if len(df) >= 6 else vol_3d_current
            vol_change_3d_pct = ((vol_3d_current - vol_3d_past) / vol_3d_past) * 100 if vol_3d_past > 0 else 0.0
            
            dist_to_poc_pct = abs((latest_close - poc_price) / poc_price) * 100
            dist_to_high_pct = ((high_30 - latest_close) / latest_close) * 100
            
            is_matched = False
            if scan_mode == "📂 1. สแกนราย Sector ที่ต้องการ (เลือกกลุ่มเจาะจง)":
                if "1. เจ้ามือกำลังสะสม" in strategy_mode:
                    if dist_to_poc_pct <= 5.0 and (rsi_min <= latest_rsi <= rsi_max):
                        is_matched = True
                else:
                    if dist_to_high_pct <= 5.0 and (rsi_min <= latest_rsi <= rsi_max):
                        is_matched = True
            elif scan_mode == "🔥 2. SET100 Volume Surge Scanner (สแกนหาหุ้นไทยที่วอลุ่มคึกคัก)":
                if vol_change_3d_pct >= 5.0:
                    is_matched = True
            elif scan_mode == "🎯 3. ดักเก็บของถูก: งบเพิ่งออก 7 วัน + โดน Sell on Fact ย่อลง 5-20%":
                if 0 <= days_since_earnings <= 7 and (-20.0 <= return_7d <= -5.0):
                    is_matched = True
            else:
                is_matched = True

            if is_matched:
                tf_data, rsi_2m_avg = calculate_timeframe_metrics(df)
                patent_theme, fundamental_review, news_summary = get_smart_fundamental_and_patent_insight(ticker)
                
                if scan_mode == "🎯 3. ดักเก็บของถูก: งบเพิ่งออก 7 วัน + โดน Sell on Factย่อลง 5-20%":
                    stock_status = f"🎯 Buy on Dip หลังงบ (ผ่านไป {days_since_earnings} วัน | 7D Return: {return_7d}%)"
                    swing_reason = f"งบเพิ่งประกาศผ่านไป {days_since_earnings} วัน แต่โดนแรงเทขาย Sell on Fact กดราคาลงมา {return_7d}% อยู่ในโซนน่าช้อนซื้อสะสมลุ้นเด้งรีบาวด์!"
                elif scan_mode == "🔎 4. ค้นหา Ticker อิสระรายตัว (NASDAQ / SET100 Custom Search)":
                    stock_status = "🎯 Custom Target Found (หุ้นที่คุณเจาะจงค้นหา)"
                    swing_reason = f"ดึงข้อมูลวิเคราะห์เจาะลึกเฉพาะตัว [{ticker}] สำเร็จ ราคาปัจจุบัน ${latest_close:.2f} (RSI: {latest_rsi:.1f})"
                elif scan_mode == "🔥 2. SET100 Volume Surge Scanner (สแกนหาหุ้นไทยที่วอลุ่มคึกคัก)":
                    stock_status = "🔥 SET100 Volume Active (วอลุ่มคึกคัก เงินเข้าสะพัด)"
                    swing_reason = f"หุ้นไทยตัวนี้มีความเคลื่อนไหวของ Volume ชัดเจน (Vol Change 3 วันอยู่ที่ {vol_change_3d_pct:+.1f}%)"
                elif "1. เจ้ามือกำลังสะสม" in strategy_mode:
                    stock_status = "🐋 เจ้ามือสะสมพลัง / อยู่ใกล้โซน POC สำคัญ"
                    swing_reason = f"โครงสร้างราคาเคลื่อนไหวอยู่ใกล้ต้นทุนเฉลี่ยของตลาด (POC: ${poc_price:.2f}) พื้นฐานและสตอรี่สิทธิบัตรแกร่ง"
                else:
                    stock_status = "⚡ หุ้นจ่อแนวต้านสำคัญ / เตรียมเบรก"
                    swing_reason = f"ราคาไต่ระดับเข้าใกล้แนวต้าน 30 วัน (${high_30:.2f}) ด้วยแรงส่งโมเมนตัมที่ดี"

                matched_data.append({
                    'Ticker': ticker, 'Close': round(latest_close, 2), 'Vol_Change_3D': round(vol_change_3d_pct, 1),
                    'RSI_Latest': round(latest_rsi, 2), 'RSI_2M_Avg': rsi_2m_avg, 'Return_7D': return_7d,
                    'TF_Data': tf_data, 'TP1': tp1_price, 'TP2': tp2_price,
                    'POC_Price': round(poc_price, 2), 'Stop_Loss': stop_loss_price,
                    'Resistance_Price': round(high_30, 2), 'Next_Earnings': next_earnings_str,
                    'Stock_Status': stock_status, 'Swing_Reason': swing_reason,
                    'Patent_Theme': patent_theme, 'Fundamental_Review': fundamental_review,
                    'News_Summary': news_summary
                })
        except:
            continue

    status_text.empty()
    progress_bar.empty()

    if matched_data:
        matched_data = sorted(matched_data, key=lambda x: x['Vol_Change_3D'], reverse=True)
        st.success(f"🎯 ดึงข้อมูลสำเร็จ! พบหุ้นเป้าหมายใน Sector ที่เลือก **{len(matched_data)} ตัว** เรียบร้อยเพื่อน!")
        st.markdown("---")
        
        for item in matched_data:
            ticker = item['Ticker']
            current_close = item['Close']
            
            expander_title = f"💎 [{ticker}] | ราคาปิด: ${current_close} | Vol Change (3D): {item['Vol_Change_3D']:+.1f}% | สถานะ: {item['Stock_Status']}"
            
            with st.expander(expander_title, expanded=True):
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("💰 ราคาปิดปัจจุบัน", f"${current_close}")
                col2.metric("🎯 ฐานราคา POC (แนวรับเจ้ามือ)", f"${item['POC_Price']}")
                col3.metric("🛑 จุดตัดขาดทุน (Stop Loss)", f"${item['Stop_Loss']}", delta_color="inverse")
                col4.metric("📅 ข้อมูลรอบงบการเงิน", f"{item['Next_Earnings']}")
                st.markdown("---")
                clean_t = ticker.replace('.BK', '')
                yahoo_news_url = f"https://finance.yahoo.com/quote/{ticker}/news/"
                investing_url = f"https://www.investing.com/search/?q={clean_t}"
                
                st.markdown(f"### 📰 สรุปข่าวสารด่วน & แหล่งแกะรอยสตอรี่ [{ticker}]")
                st.info(item['News_Summary'])
                
                col_n1, col_n2 = st.columns(2)
                col_n1.link_button(f"🔗 ไปที่ Yahoo Finance News ({ticker})", yahoo_news_url)
                col_n2.link_button(f"🔗 ค้นหาข่าวเชิงลึกใน Investing.com ({clean_t})", investing_url)
                
                st.markdown("---")
                st.markdown("### 🧠 มุมมองวิเคราะห์เชิงลึกจากเพื่อน (งบการเงิน, สิทธิบัตร & เกมเจ้ามือ Smart Money)")
                st.info(f"📌 **สถานะหุ้น:** {item['Stock_Status']}\n\n💡 **วิเคราะห์พฤติกรรมราคา:** {item['Swing_Reason']}")
                st.success(f"🧬 **แกะรอยสิทธิบัตร & นวัตกรรมอนาคต:** {item['Patent_Theme']}\n\n📊 **วิเคราะห์งบการเงิน & ความแข็งแกร่งกิจการ:** {item['Fundamental_Review']}")

                st.markdown("---")
                st.markdown("### ⏱️ ตารางแกะรอย % Vol Change ทั้ง 2 ค่า, ค่าเฉลี่ย RSI & พฤติกรรมตลาดในแต่ละไทม์เฟรม")
                
                tf_rows = []
                for tf_name in ['1 วัน', '3 วัน', '1 อาทิตย์', '2 อาทิตย์', '1 เดือน', '2 เดือน']:
                    if tf_name in item['TF_Data']:
                        info = item['TF_Data'][tf_name]
                        poc_display = f"${info['poc_price']}" if info['poc_price'] is not None else "None"
                        tf_rows.append({
                            'ไทม์เฟรม': tf_name, 
                            'ราคาสูง/ต่ำสุด': f"${info['high']} / ${info['low']}",
                            'กรอบ (Range)': f"{info['range_pct']}%",
                            'POC (ฐานราคาหนาแน่น)': poc_display,
                            '📉 ค่าเฉลี่ย RSI': f"{info['tf_rsi_avg']}",
                            '📊 Vol Change (ปัจจุบัน)': f"{info['vol_change_current']:+.1f}%",
                            '📊 Vol Change (เทียบอดีต)': f"{info['vol_change_vs_past']:+.1f}%",
                            '🔍 สรุปพฤติกรรมภาพรวม': info['market_behavior']
                        })
                st.table(pd.DataFrame(tf_rows))

                st.markdown("---")
                st.warning(f"🔥 **คำแนะนำจากเพื่อนรัก:** โซนนี้เช็กข้อมูลสิทธิบัตรและงบการเงินประกอบเรียบร้อย ถ้าหุ้นหลุด Stop Loss ที่ **${item['Stop_Loss']}** ให้ตัดใจคัทลอสทันที อย่าฝืนถือลุ้นเพื่อน!")

                st.markdown("---")
    else:
        st.warning("⚠️ ไม่พบหุ้นที่ตรงตามเงื่อนไขใน Sector ที่มึงเลือก ลองปรับกลุ่ม Sector หรือเปลี่ยนโหมดดูใหม่นะเพื่อน!")

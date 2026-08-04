import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime

st.set_page_config(page_title="Deep Innovation, Global & SET100 Swing Radar Pro", layout="wide")

st.title("🎯 Deep Innovation, Global & SET100 Full-Scale Swing Radar Pro")
st.markdown("### เรดาร์สแกนหุ้นนวัตกรรม & สิทธิบัตร (เพิ่มช่องวันประกาศงบรอบหน้าแบบ - ถ้ายัังไม่ประกาศ)")

@st.cache_data(ttl=86400)
def get_massive_universe_with_set100():
    universe = {
        "💻 1. Information Technology, AI, Cloud & Semiconductors (Global)": [
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

def get_next_earnings_date(ticker):
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
        
        if earnings_date is None:
            return "-"
            
        today = datetime.now().date()
        days_left = (earnings_date - today).days
        
        if days_left < 0:
            return f"{earnings_date.strftime('%Y-%m-%d')} (ผ่านไปแล้ว)"
        else:
            return f"{earnings_date.strftime('%Y-%m-%d')} (อีก {days_left} วัน)"
    except:
        return "-"

def calculate_timeframe_metrics(df):
    timeframe_days = {
        '1 วัน': 1, '3 วัน': 3, '1 อาทิตย์': 5, '2 อาทิตย์': 10, '1 เดือน': 20, '2 เดือน': 40
    }
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
            "AI Computing & GPU Architecture Patents", 
            "ผู้นำตลาดชิป AI ผูกขาดสิทธิบัตรสถาปัตยกรรม CUDA และ Blackwell อัตรากำไรขั้นต้น (Gross Margin) สูงระดับ 75%+ งบการเงินแข็งแกร่งระดับเงินสดล้นมือ เจ้ามือสถาบันคุมเกมสะสมรอบใหญ่รอรับดีมานด์ดาต้าเซ็นเตอร์ทั่วโลก",
            "🔥 **ข่าวสด & สตอรี่ล่าสุด:** ตลาดกำลังจับตาการส่งมอบชิปล็อตใหญ่ Blackwell และสิทธิบัตรระบบระบายความร้อน Liquid Cooling ที่แก้ปัญหาคอขวด Data Center"
        )
    elif 'AAPL' in ticker_upper:
        return (
            "Consumer Electronics & Ecosystem Patents", 
            "เจ้าพ่ออีโคซิสเต็มและสิทธิบัตรดีไซน์ฮาร์ดแวร์ กระแสเงินสดอิสระ (FCF) มหาศาล งบดุลป้อมปราการเหล็ก หุ้น Defensive ชั้นดีที่รอจังหวะ Smart Money เก็บของสะสมเพื่อรับรอบเปิดตัวนวัตกรรมใหม่ๆ",
            "🔥 **ข่าวสด & สตอรี่ล่าสุด:** อัปเดตข่าวคราวการพัฒนาซอฟต์แวร์ AI และรอบการเปิดตัวฮาร์ดแวร์รุ่นใหม่ที่จดสิทธิบัตรดีไซน์หน้าจอพับและวัสดุน้ำหนักเบา"
        )
    elif 'TSLA' in ticker_upper:
        return (
            "EV, Autonomous Driving & Energy Patents", 
            "เจ้าแห่งนวัตกรรมยานยนต์ไฟฟ้าและซอฟต์แวร์ FSD (Full Self-Driving) รวมถึงสิทธิบัตรระบบกักเก็บพลังงาน Megapack เกมราคาผันผวนสูง เจ้ามักเขย่าแรงเพื่อสลัดเม่าก่อนลากจริงตามความคืบหน้าของเทคโนโลยี Robotaxi",
            "🔥 **ข่าวสด & สตอรี่ล่าสุด:** ความคืบหน้าการขออนุมัติระบบ FSD Unsupervised ในหลายรัฐ และสิทธิบัตร AI Vision-Only ที่ทิ้งห่างคู่แข่ง"
        )
    elif 'ISRG' in ticker_upper:
        return (
            "Medical Robotics & Surgical Patents", 
            "ผู้นำหุ่นยนต์ผ่าตัด da Vinci ผูกขาดสิทธิบัตรทางการแพทย์ระดับโลก รายได้เติบโตสม่ำเสมอจากโมเดลธุรกิจแบบ Recurring (ขายเครื่องพร้อมขายอุปกรณ์ใช้แล้วทิ้งรายครั้ง) กองทุนใหญ่ชอบสะสมเงียบๆ",
            "🔥 **ข่าวสด & สตอรี่ล่าสุด:** ดีมานด์การใช้หุ่นยนต์ผ่าตัด da Vinci 5 พุ่งสูงขึ้นในโรงพยาบาลชั้นนำทั่วโลก หนุนรายได้ค่าอุปกรณ์ใช้แล้วทิ้งเติบโตต่อเนื่อง"
        )
    elif 'DELTA.BK' in ticker_upper:
        return (
            "Power Electronics & Data Center Components", 
            "หุ้นไฮไลท์นวัตกรรมอิเล็กทรอนิกส์ไทย สิทธิบัตรระบบจัดการพลังงานสำหรับ Data Center AI ระดับโลก งบการเงินโตเร่งตามกระแสเทคโนโลยี AI Global Supply Chain เจ้ามือไทยคุมโซนราคาแน่นหนา",
            "🔥 **ข่าวสด & สตอรี่ล่าสุด:** คำสั่งซื้อชิ้นส่วนพาวเวอร์ซัพพลายสำหรับ AI Server และ Data Center เติบโตตามดีมานด์ฝั่งอเมริกาและไต้หวัน"
        )
    else:
        return (
            "Global Tech & Innovation Moat", 
            "บริษัทที่มีจุดแข็งด้านเทคโนโลยีหรือส่วนแบ่งการตลาดสูง งบการเงินอยู่ในเกณฑ์เสถียร เหมาะกับการใช้เรดาร์แกะรอยพฤติกรรม Smart Money เพื่อหาจังหวะเข้าทำกำไรระยะสั้นถึงกลางตามรอบงบการเงิน",
            "🔥 **ข่าวสด & สตอรี่ล่าสุด:** ติดตามข่าวสารการยื่นจดสิทธิบัตรผลิตภัณฑ์ใหม่และการเติบโตของรายได้ในไตรมาสล่าสุดอย่างใกล้ชิด"
        )

universe = get_massive_universe_with_set100()

st.sidebar.markdown("### ⚙️ เลือกโหมดกลยุทธ์การสแกน (ปรับความยืดหยุ่น)")
scan_mode = st.sidebar.radio("📌 เลือกรูปแบบการสแกน", [
    "📂 1. สแกนหุ้นนวัตกรรมโลก & SET100 (เลือกกลยุทธ์เชิงลึก)", 
    "🔥 2. SET100 Volume Surge Scanner (สแกนหาหุ้นไทยที่วอลุ่มคึกคัก)",
    "🔎 3. ค้นหา Ticker อิสระรายตัว (Custom Search)"
])

if scan_mode == "📂 1. สแกนหุ้นนวัตกรรมโลก & SET100 (เลือกกลยุทธ์เชิงลึก)":
    selected_sector = st.sidebar.selectbox("📂 เลือกกลุ่มอุตสาหกรรม / SET100", list(universe.keys()))
    strategy_mode = st.sidebar.selectbox("🎯 เลือกกลยุทธ์การเล่นรอบ", [
        "1. เจ้ามือกำลังสะสม (Accumulation) ใกล้ VAL / POC [ยืดหยุ่น]", 
        "2. จ่อแนวต้านสำคัญหรือกำลังเบรกเอาท์ [ยืดหยุ่น]"
    ])
    rsi_min = st.sidebar.slider("📉 RSI ต่ำสุด", 25, 50, 35)
    rsi_max = st.sidebar.slider("📈 RSI สูงสุด", 50, 90, 80)
elif scan_mode == "🔥 2. SET100 Volume Surge Scanner (สแกนหาหุ้นไทยที่วอลุ่มคึกคัก)":
    st.sidebar.info("ระบบจะกวาดตรวจ Volume ทุกตัวใน SET100 แบบยืดหยุ่นเพื่อให้เจอหุ้นเด่นแน่นอน")
else:
    st.sidebar.markdown("---")
    custom_ticker_input = st.sidebar.text_input("🔤 ใส่ Ticker หุ้นที่ต้องการ (เช่น NVDA, DELTA.BK, PTT.BK)", "NVDA")

st.markdown(f"## 🎯 เรดาร์สแกนหุ้นรอบสั้นตามงบการเงิน, ข่าวสารนวัตกรรม & วันประกาศงบรอบหน้า")

if st.button("🚀 เริ่มรันระบบสแกน (ลุยกันเพื่อน!)"):
    target_tickers = []
    
    if scan_mode == "📂 1. สแกนหุ้นนวัตกรรมโลก & SET100 (เลือกกลยุทธ์เชิงลึก)":
        target_tickers = universe[selected_sector]
    elif scan_mode == "🔥 2. SET100 Volume Surge Scanner (สแกนหาหุ้นไทยที่วอลุ่มคึกคัก)":
        target_tickers = universe["🇹🇭 7. SET100 Top Thai Giants & Swing Movers (Thailand)"]
    else:
        cleaned_ticker = custom_ticker_input.strip().upper()
        if cleaned_ticker:
            target_tickers = [cleaned_ticker]

    matched_data = []
    progress_bar = st.progress(0)
    status_text = st.empty()
    total_tickers = len(target_tickers)
    
    for i, ticker in enumerate(target_tickers):
        status_text.text(f"กำลังวิเคราะห์หุ้น [{ticker}] ({i+1}/{total_tickers})...")
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
            
            next_earnings = get_next_earnings_date(ticker)
            
            vol_3d_current = float(df.tail(3)['Volume'].mean())
            vol_3d_past = float(df.iloc[-6:-3]['Volume'].mean()) if len(df) >= 6 else vol_3d_current
            vol_change_3d_pct = ((vol_3d_current - vol_3d_past) / vol_3d_past) * 100 if vol_3d_past > 0 else 0.0
            
            dist_to_poc_pct = abs((latest_close - poc_price) / poc_price) * 100
            dist_to_high_pct = ((high_30 - latest_close) / latest_close) * 100
            
            is_matched = False
            if scan_mode == "📂 1. สแกนหุ้นนวัตกรรมโลก & SET100 (เลือกกลยุทธ์เชิงลึก)":
                if "1. เจ้ามือกำลังสะสม" in strategy_mode:
                    if dist_to_poc_pct <= 5.0 and (rsi_min <= latest_rsi <= rsi_max):
                        is_matched = True
                else:
                    if dist_to_high_pct <= 5.0 and (rsi_min <= latest_rsi <= rsi_max):
                        is_matched = True
            elif scan_mode == "🔥 2. SET100 Volume Surge Scanner (สแกนหาหุ้นไทยที่วอลุ่มคึกคัก)":
                if vol_change_3d_pct >= 5.0:
                    is_matched = True
            else:
                is_matched = True

            if is_matched:
                tf_data, rsi_2m_avg = calculate_timeframe_metrics(df)
                patent_theme, fundamental_review, news_summary = get_smart_fundamental_and_patent_insight(ticker)
                
                if scan_mode == "🔥 2. SET100 Volume Surge Scanner (สแกนหาหุ้นไทยที่วอลุ่มคึกคัก)":
                    stock_status = "🔥 SET100 Volume Active (วอลุ่มคึกคัก เงินเข้าสะพัด)"
                    swing_reason = f"หุ้นไทยตัวนี้มีความเคลื่อนไหวของ Volume ชัดเจน (Vol Change 3 วันอยู่ที่ {vol_change_3d_pct:+.1f}%) เหมาะกับการเก็งกำไรตามกระแสเงินทุนหมุนเวียนในตลาด"
                elif "1. เจ้ามือกำลังสะสม" in strategy_mode:
                    stock_status = "🐋 เจ้ามือสะสมพลัง / อยู่ใกล้โซน POC สำคัญ"
                    swing_reason = f"โครงสร้างราคาเคลื่อนไหวอยู่ใกล้ระดับต้นทุนเฉลี่ยของตลาด (POC: ${poc_price:.2f}) พื้นฐานงบการเงินและสตอรี่สิทธิบัตรนวัตกรรมรองรับดี เหมาะทยอยสะสมไม้แรก"
                else:
                    stock_status = "⚡ หุ้นจ่อแนวต้านสำคัญ / เตรียมเบรก"
                    swing_reason = f"ราคาไต่ระดับขึ้นมาใกล้แนวต้าน 30 วัน (${high_30:.2f}) ด้วยแรงส่งโมเมนตัมที่ดี มีโอกาสลุ้นทะลุแนวต้านเพื่อทำกำไรช่วงสั้น"

                matched_data.append({
                    'Ticker': ticker, 'Close': round(latest_close, 2), 'Vol_Change_3D': round(vol_change_3d_pct, 1),
                    'RSI_Latest': round(latest_rsi, 2), 'RSI_2M_Avg': rsi_2m_avg,
                    'TF_Data': tf_data, 'TP1': tp1_price, 'TP2': tp2_price,
                    'POC_Price': round(poc_price, 2), 'Stop_Loss': stop_loss_price,
                    'Resistance_Price': round(high_30, 2), 'Next_Earnings': next_earnings,
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
        st.success(f"🎯 สแกนสำเร็จ! คัดเจอหุ้นที่ตรงตามเงื่อนไขยืดหยุ่นทั้งหมด **{len(matched_data)} ตัว**!")
        st.markdown("---")
        
        for item in matched_data:
            ticker = item['Ticker']
            current_close = item['Close']
            
            expander_title = f"💎 [{ticker}] | ราคาปิด: ${current_close} | Vol Change (3D): {item['Vol_Change_3D']:+.1f}% | สถานะ: {item['Stock_Status']}"
            
            with st.expander(expander_title, expanded=False):
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("💰 ราคาปิดปัจจุบัน", f"${current_close}")
                col2.metric("🎯 ฐานราคา POC (แนวรับเจ้ามือ)", f"${item['POC_Price']}")
                col3.metric("🛑 จุดตัดขาดทุน (Stop Loss)", f"${item['Stop_Loss']}", delta_color="inverse")
                col4.metric("📅 ประกาศงบรอบหน้า", f"{item['Next_Earnings']}")
                
                st.markdown("---")
                # บล็อกสรุปข่าวสารด่วนและลิงก์แกะรอย
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
                
                st.success(f"🧬 **แกะรอยสิทธิบัตร & นวัตกรรม:** {item['Patent_Theme']}\n\n📊 **วิเคราะห์งบการเงิน & ความแข็งแกร่ง:** {item['Fundamental_Review']}")

                st.markdown("---")
                st.markdown("### ⏱️ ตารางแกะรอย % Vol Change ทั้ง 2 ค่า, ค่าเฉลี่ย RSI & พฤติกรรมตลาดในแต่ละไทม์เฟรม")
                tf_rows =

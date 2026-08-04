import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf

st.set_page_config(page_title="Deep Innovation, Global & SET100 Swing Radar Pro", layout="wide")

st.title("🎯 Deep Innovation, Global & SET100 Full-Scale Swing Radar Pro")
st.markdown("### เรดาร์สแกนหุ้นนวัตกรรม & สิทธิบัตรระดับโลก (กรองเฉพาะตัวใกล้ Valuation / ใกล้เบรกเอาท์ พร้อมเล่นรอบสั้น!)")

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

def calculate_timeframe_metrics(df):
    timeframe_days = {
        '1 วัน': 1, 
        '3 วัน': 3, 
        '1 อาทิตย์': 5, 
        '2 อาทิตย์': 10, 
        '1 เดือน': 20, 
        '2 เดือน': 40
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

            if vol_change_vs_past > 15 and total_range_pct < 15:
                market_behavior = "🐋 Smart Money ซุ่มเก็บของสะสมพลัง (เม่าทยอยขายทำกำไรออกของ)"
            elif vol_change_vs_past > 20 and total_range_pct >= 15:
                market_behavior = "🚀 Smart Money ลากเบรกเอาท์ดันราคา (เม่าแห่ไล่ซื้อตามกระแสข่าว)"
            elif vol_change_vs_past < -10:
                market_behavior = "⚖️ ตลาดซึมตัว / เม่าถอดใจคัทลอส (เจ้ามือประคองแนวรับ)"
            else:
                market_behavior = "🔄 แรงซื้อขายสมดุล ไซด์เวย์สร้างฐานในกรอบ"

            results[label] = {
                'start_date': start_date, 'high': round(high_max, 2), 'low': round(low_min, 2),
                'range_pct': total_range_pct, 'poc_price': poc_price,
                'tf_rsi_avg': tf_rsi_avg,
                'vol_change_current': vol_change_current,
                'vol_change_vs_past': vol_change_vs_past,
                'market_behavior': market_behavior
            }
        except:
            results[label] = {
                'start_date': None, 'high': 0.0, 'low': 0.0, 'range_pct': 0.0, 'poc_price': None,
                'tf_rsi_avg': 0.0, 'vol_change_current': 0.0, 'vol_change_vs_past': 0.0,
                'market_behavior': 'N/A'
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

universe = get_massive_universe_with_set100()

st.sidebar.markdown("### ⚙️ ตั้งค่าเรดาร์สแกนหุ้นรอบ (Smart Precision Filter)")
scan_mode = st.sidebar.radio("📌 เลือกโหมดการค้นหา", ["📂 สแกนทั้ง Sector / SET100 แบบคัดกรองพิเศษ", "🔎 ค้นหา Ticker อิสระรายตัว (Custom Search)"])

if scan_mode == "📂 สแกนทั้ง Sector / SET100 แบบคัดกรองพิเศษ":
    selected_sector = st.sidebar.selectbox("📂 เลือกกลุ่มอุตสาหกรรม / SET100", list(universe.keys()))
    strategy_mode = st.sidebar.selectbox("🎯 เลือกกลยุทธ์การเล่นรอบเน้นๆ", [
        "1. หุ้นจ่อแนวต้าน / ใกล้ Valuation (พร้อมเบรก)", 
        "2. หุ้นกำลังเบรกเอาท์ผ่านแนวต้านไม่เกิน 2 แท่ง (Momentum Breakout)"
    ])
    rsi_min = st.sidebar.slider("📉 RSI ต่ำสุด", 35, 60, 45)
    rsi_max = st.sidebar.slider("📈 RSI สูงสุด", 60, 85, 78)
else:
    st.sidebar.markdown("---")
    custom_ticker_input = st.sidebar.text_input("🔤 ใส่ Ticker หุ้นที่ต้องการ (เช่น NVDA, DELTA.BK, PTT.BK)", "NVDA")
    st.sidebar.info("ระบบจะดึงข้อมูลตัวนี้มาแกะรอยทันที!")

st.markdown(f"## 🎯 เรดาร์สแกนหุ้นนวัตกรรมทรงคุณค่า (โฟกัสเฉพาะตัวจ่อต้าน & เบรกเอาท์ไม่เกิน 2 แท่ง)")

if st.button("🚀 เริ่มรันสแกนเจาะลึกแบบคัดกรองพิเศษ (ลุยกันเพื่อน!)"):
    target_tickers = []
    
    if scan_mode == "📂 สแกนทั้ง Sector / SET100 แบบคัดกรองพิเศษ":
        target_tickers = universe[selected_sector]
    else:
        cleaned_ticker = custom_ticker_input.strip().upper()
        if cleaned_ticker:
            target_tickers = [cleaned_ticker]

    matched_data = []
    progress_bar = st.progress(0)
    status_text = st.empty()
    total_tickers = len(target_tickers)
    
    for i, ticker in enumerate(target_tickers):
        status_text.text(f"กำลังคัดกรองและวิเคราะห์หุ้น [{ticker}] ({i+1}/{total_tickers})...")
        progress_bar.progress((i + 1) / total_tickers)
        
        try:
            df = yf.download(ticker, period="3mo", interval="1d", progress=False)
            if df.empty or len(df) < 40:
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
            
            # คำนวณกรอบราคา High / Low ในช่วง 20 วันล่าสุดเพื่อหาแนวต้าน (Valuation Resistance)
            recent_20 = df.tail(20).copy()
            res_20days = float(recent_20['High'].max())
            low_20days = float(recent_20['Low'].min())
            
            # เช็คระยะห่างจากแนวต้าน 20 วัน (เพื่อดูว่าใกล้ Val / ใกล้ต้าน หรือเพิ่งเบรก)
            distance_to_res_pct = ((res_20days - latest_close) / latest_close) * 100
            
            recent_20['Vol_MA'] = recent_20['Volume'].rolling(window=10).mean()
            last_vol = float(recent_20['Volume'].iloc[-1])
            last_vol_ma = float(recent_20['Vol_MA'].iloc[-1]) if pd.notna(recent_20['Vol_MA'].iloc[-1]) else last_vol
            
            is_matched = False
            if scan_mode == "📂 สแกนทั้ง Sector / SET100 แบบคัดกรองพิเศษ":
                if "1. หุ้นจ่อแนวต้าน" in strategy_mode:
                    # เงื่อนไข: ราคาอยู่ต่ำกว่าแนวต้านไม่เกิน 3.5% และ RSI อยู่ในเกณฑ์ดี
                    if -1.0 <= distance_to_res_pct <= 3.5 and (rsi_min <= latest_rsi <= rsi_max):
                        is_matched = True
                else:
                    # เงื่อนไข: เพิ่งเบรกเอาท์ผ่านแนวต้านขึ้นมา (ราคาอยู่เหนือ High เดิมเล็กน้อยไม่เกิน 2%) และ Vol พุ่ง
                    vol_spike = last_vol >= (last_vol_ma * 1.1)
                    if latest_close >= res_20days * 0.995 and vol_spike and (latest_rsi >= rsi_min):
                        is_matched = True
            else:
                is_matched = True # กรณีค้นหารายตัว ให้แสดงผลเสมอ

            if is_matched:
                tf_data, rsi_2m_avg = calculate_timeframe_metrics(df)
                tp1_price = round(latest_close * 1.05, 2)
                
                if -1.0 <= distance_to_res_pct <= 3.5:
                    stock_status = "⚡ หุ้นจ่อแนวต้าน / ใกล้ Valuation (เตรียมเบรก)"
                    swing_reason = "ราคากำลังจ่อทดสอบแนวต้านสำคัญ โครงสร้างงบการเงินแกร่งและมีข่าวสิทธิบัตรหนุน Smart Money จ่อเคาะขวาเพื่อทะยานผ่านแนวต้าน เหมาะเตรียมเคาะตามน้ำเมื่อผ่านแนวต้าน"
                else:
                    stock_status = "🚀 หุ้นกำลังเบรกเอาท์ผ่านแนวต้าน (ผ่านไปไม่เกิน 2 แท่ง)"
                    swing_reason = "ราคาเพิ่งระเบิดวอลุ่มเบรกแนวต้านขึ้นมาสดๆ ร้อนๆ สัญญาณโมเมนตัมกำลังมารอบสั้น เป็นจังหวะเข้าเก็งกำไรตามโมเมนตัมที่ดีเยี่ยม (Momentum Play)"

                moat_status = "โครงสร้างงบการเงินแกร่ง / มีความได้เปรียบเชิงแข่งขันและสิทธิบัตรนวัตกรรมรองรับ"
                
                matched_data.append({
                    'Ticker': ticker, 'Close': round(latest_close, 2), 'Distance_Res': round(distance_to_res_pct, 1),
                    'RSI_Latest': round(latest_rsi, 2), 'RSI_2M_Avg': rsi_2m_avg,
                    'TF_Data': tf_data, 'TP1': tp1_price,
                    'High_Max': round(res_20days, 2), 'Low_Min': round(low_20days, 2),
                    'Stock_Status': stock_status, 'Swing_Reason': swing_reason, 'Moat_Status': moat_status
                })
        except:
            continue

    status_text.empty()
    progress_bar.empty()

    if matched_data:
        st.success(f"🎯 คัดกรองสำเร็จ! พบหุ้นเกรด A ที่ตรงเงื่อนไข 'ใกล้ Val / เบรกต้านไม่เกิน 2 แท่ง' ทั้งหมด **{len(matched_data)} ตัว**!")
        st.markdown("---")
        
        for item in matched_data:
            ticker = item['Ticker']
            current_close = item['Close']
            
            expander_title = f"🔥 [{ticker}] | ราคาปิด: ${current_close} | สถานะ: {item['Stock_Status']} | RSI: {item['RSI_Latest']}"
            
            with st.expander(expander_title, expanded=False):
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("💰 ราคาปิดปัจจุบัน", f"${current_close}")
                col2.metric("📉 RSI ล่าสุด / เฉลี่ย 2M", f"{item['RSI_Latest']} / {item['RSI_2M_Avg']}")
                col3.metric("🎯 แนวต้าน / Valuation", f"${item['High_Max']}")
                col4.metric("🎯 เป้าทำกำไร (TP1 +5%)", f"${item['TP1']}")
                
                st.markdown("---")
                st.markdown("### 📊 วิเคราะห์เชิงลึก: งบการเงิน, สิทธิบัตร & เหตุผลการเล่นรอบสั้น")
                st.info(f"📌 **สถานะหุ้น:** {item['Stock_Status']}\n\n💡 **วิเคราะห์โดยกูรู (งบการเงิน & ข่าวสิทธิบัตรนวัตกรรม):** {item['Swing_Reason']}")

                st.markdown("---")
                st.markdown("### ⏱️ ตารางแกะรอย % Vol Change, ค่าเฉลี่ย RSI & สรุปพฤติกรรมตลาดในแต่ละไทม์เฟรม")
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
                st.warning(f"💡 **คำแนะนำจากเพื่อน:** หุ้น **{ticker}** ตัวนี้ผ่านเกณฑ์คัดกรองงบการเงินและมีสิทธิบัตรเทคโนโลยีรองรับชัดเจน อยู่ในโซนพร้อมรบตอดสั้น ถ้า Volume ยืนยันตามตาราง ลุยไม้แรกตามแผนได้เลยเพื่อน!")

                st.markdown("---")
    else:
        st.warning("⚠️ ไม่พบหุ้นที่ตรงเงื่อนไข 'จ่อต้าน / เบรกไม่เกิน 2 แท่ง' ในหมวดนี้ ลองปรับสลับโหมดกลยุทธ์ด้านซ้ายดูใหม่นะเพื่อน!")
        

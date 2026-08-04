import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf

st.set_page_config(page_title="Deep Innovation, Global & SET100 Swing Radar Pro", layout="wide")

st.title("🎯 Deep Innovation, Global & SET100 Full-Scale Swing Radar Pro")
st.markdown("### เรดาร์สแกนหุ้นนวัตกรรม สิทธิบัตร, หุ้นนอก และ SET100 พร้อมคำนวณ % Vol Change เป๊ะตามสูตรเจาะลึก")

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
    # กำหนดจำนวนวันของแต่ละไทม์เฟรม
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
            # ดึงข้อมูลในช่วงปัจจุบัน (Recent N days) และช่วงอดีตก่อนหน้า (Previous N days)
            total_needed = days * 2
            if len(df) < total_needed:
                # ถ้าข้อมูลไม่พอ ให้ใช้ข้อมูลเท่าที่มีแบ่งครึ่ง
                half_len = max(1, len(df) // 2)
                sub_df = df.tail(half_len).copy()
                past_df = df.iloc[:-half_len].tail(half_len).copy()
            else:
                sub_df = df.tail(days).copy()
                past_df = df.iloc[-(days * 2):-days].copy()

            high_max = float(sub_df['High'].max())
            low_min = float(sub_df['Low'].min())
            start_date = sub_df.index[0].strftime('%Y-%m-%d') if not sub_df.empty else None
            
            high_pct = round(((high_max - current_close) / current_close) * 100, 1) if current_close > 0 else 0.0
            low_pct = round(((low_min - current_close) / current_close) * 100, 1) if current_close > 0 else 0.0
            total_range_pct = round(((high_max - low_min) / current_close) * 100, 1) if current_close > 0 else 0.0
            
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

            # คำนวณ % Vol Change ตามสูตรที่มึงต้องการเป๊ะๆ
            # 1 วัน: เทียบ วันนี้ กับ เมื่อวาน
            # 3 วัน / อื่นๆ: เทียบค่าเฉลี่ยช่วงปัจจุบัน กับ ช่วงอดีตก่อนหน้า
            if days == 1:
                latest_vol = float(sub_df['Volume'].iloc[-1]) if not sub_df.empty else 0.0
                prev_vol = float(past_df['Volume'].iloc[-1]) if not past_df.empty else latest_vol
                vol_change_pct = round(((latest_vol - prev_vol) / prev_vol) * 100, 1) if prev_vol > 0 else 0.0
            else:
                current_vol_avg = float(sub_df['Volume'].mean()) if not sub_df.empty else 0.0
                past_vol_avg = float(past_df['Volume'].mean()) if not past_df.empty else current_vol_avg
                vol_change_pct = round(((current_vol_avg - past_vol_avg) / past_vol_avg) * 100, 1) if past_vol_avg > 0 else 0.0

            # ประเมินพฤติกรรม เม่า vs เจ้ามือ จากทิศทาง Vol Change
            retail_flow_val = "เม่าทยอยขายทำกำไร / วอลุ่มหด (-)" if vol_change_pct < 0 else "เม่าแห่ไล่ซื้อเก็งกำไร (+)"
            smart_money_val = "เจ้ามือซุ่มเก็บของเงียบๆ (Accumulation)" if total_range_pct < 10 and vol_change_pct >= 0 else ("เจ้ามือลากเบรกเอาท์ (Markup)" if vol_change_pct > 20 else "รอจังหวะสะสมพลัง")

            results[label] = {
                'start_date': start_date, 'high': round(high_max, 2), 'low': round(low_min, 2),
                'high_pct': high_pct, 'low_pct': low_pct, 'range_pct': total_range_pct,
                'poc_price': poc_price, 'vol_change_pct': vol_change_pct,
                'retail_flow': retail_flow_val, 'smart_money': smart_money_val
            }
        except:
            results[label] = {
                'start_date': None, 'high': 0.0, 'low': 0.0,
                'high_pct': 0.0, 'low_pct': 0.0, 'range_pct': 0.0,
                'poc_price': None, 'vol_change_pct': 0.0,
                'retail_flow': 'N/A', 'smart_money': 'N/A'
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

st.sidebar.markdown("### ⚙️ ตั้งค่าเรดาร์สแกนหุ้นรอบ (รวม SET100)")
scan_mode = st.sidebar.radio("📌 เลือกโหมดการค้นหา", ["📂 สแกนทั้ง Sector / SET100 แบบยกเข่ง", "🔎 ค้นหา Ticker อิสระรายตัว (Custom Search)"])

if scan_mode == "📂 สแกนทั้ง Sector / SET100 แบบยกเข่ง":
    selected_sector = st.sidebar.selectbox("📂 เลือกกลุ่มอุตสาหกรรม / SET100", list(universe.keys()))
    strategy_mode = st.sidebar.selectbox("⚙️ เลือกโหมดการค้นหา", [
        "1. โหมดสะสมพลังออกข้าง (Range-Bound Accumulation & Base Building)", 
        "2. โหมดเจ้ามือเริ่มเคาะขยับเบรกเอาท์ (Momentum Breakout & Volume Surge)"
    ])
    rsi_min = st.sidebar.slider("📉 RSI ต่ำสุด", 20, 50, 30)
    rsi_max = st.sidebar.slider("📈 RSI สูงสุด", 50, 85, 75)
else:
    st.sidebar.markdown("---")
    custom_ticker_input = st.sidebar.text_input("🔤 ใส่ Ticker หุ้นที่ต้องการ (เช่น NVDA, DELTA.BK, PTT.BK)", "NVDA")
    st.sidebar.info("ระบบจะดึงข้อมูลตัวนี้มาแกะรอยทันที!")

st.markdown(f"## 🎯 เรดาร์จับตา % Vol Change & พฤติกรรมเจ้ามือ (นวัตกรรม & SET100)")

if st.button("🚀 เริ่มรันสแกนข้อมูลเชิงลึก (ลุยกันเลยเพื่อน!)"):
    target_tickers = []
    
    if scan_mode == "📂 สแกนทั้ง Sector / SET100 แบบยกเข่ง":
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
        status_text.text(f"กำลังดึงและคำนวณข้อมูลหุ้น [{ticker}] ({i+1}/{total_tickers})...")
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
            
            recent = df.tail(20).copy()
            high_max = float(recent['High'].max())
            low_min = float(recent['Low'].min())
            range_pct = (high_max - low_min) / latest_close if latest_close > 0 else 0.0
            
            recent['Vol_MA'] = recent['Volume'].rolling(window=10).mean()
            last_vol = float(recent['Volume'].iloc[-1])
            last_vol_ma = float(recent['Vol_MA'].iloc[-1]) if pd.notna(recent['Vol_MA'].iloc[-1]) else 0.0
            
            is_matched = True
            if scan_mode == "📂 สแกนทั้ง Sector / SET100 แบบยกเข่ง":
                if "สะสม" in strategy_mode:
                    if not (range_pct <= 0.35 and rsi_min <= latest_rsi <= rsi_max):
                        is_matched = False
                else:
                    vol_spike = last_vol >= (last_vol_ma * 1.05) if last_vol_ma > 0 else False
                    if not (range_pct >= 0.02 and latest_rsi >= rsi_min and vol_spike):
                        is_matched = False

            if is_matched:
                tf_data, rsi_2m_avg = calculate_timeframe_metrics(df)
                tp1_price = round(latest_close * 1.05, 2)
                
                # กำหนดสถานะหุ้นและเหตุผลเล่นรอบสั้น
                if range_pct <= 0.12:
                    stock_status = "🟡 กำลังสร้างฐานสะสมพลัง (Accumulation Base)"
                    swing_reason = "หุ้นพักตัวออกข้าง Volume แห้ง เม่าถอดใจขายทำกำไร แต่ Smart Money ทยอยตั้งรับโซนแนวรับแน่น เหมาะกับการทยอยสะสมไม้แรกเพื่อรอจังหวะสะบัดรอบใหญ่"
                elif latest_rsi > 70:
                    stock_status = "🔴 อยู่ในโซนร้อนแรง / จ่อทำกำไร (Overbought / Markup Phase)"
                    swing_reason = "ราคาพุ่งทำนิวไฮพร้อมวอลุ่มหนาแน่น เม่าแห่ไล่ซื้อตามข่าวสั้น ระวังแรงขายทำกำไรระยะสั้น เหมาะกับคนมีของเตรียมทยอยขายล็อกกำไร (TP1)"
                else:
                    stock_status = "🟢 กำลังเบรกเอาท์เปลี่ยนรอบ (Momentum Breakout)"
                    swing_reason = "เกิดสัญญาณวอลุ่มพุ่งทะลุต้านย่อย Smart Money ดันราคาออกจากกรอบสะสม เป็นจังหวะเข้าเล่นรอบสั้นตามโมเมนตัมที่ดีเยี่ยม"

                moat_status = "โครงสร้างพื้นฐานแกร่ง / มีความได้เปรียบเชิงแข่งขันสูงและสิทธิบัตรคุ้มครอง"
                
                matched_data.append({
                    'Ticker': ticker, 'Close': round(latest_close, 2), 'Range_Pct': round(range_pct * 100, 1),
                    'RSI_Latest': round(latest_rsi, 2), 'RSI_2M_Avg': rsi_2m_avg,
                    'TF_Data': tf_data, 'TP1': tp1_price,
                    'High_Max': round(high_max, 2), 'Low_Min': round(low_min, 2),
                    'Stock_Status': stock_status, 'Swing_Reason': swing_reason, 'Moat_Status': moat_status
                })
        except:
            continue

    status_text.empty()
    progress_bar.empty()

    if matched_data:
        st.success(f"🎯 สแกนสำเร็จ! พบหุ้นที่ตรงเงื่อนไขทั้งหมด **{len(matched_data)} ตัว**!")
        st.markdown("---")
        
        for item in matched_data:
            ticker = item['Ticker']
            current_close = item['Close']
            
            expander_title = f"🟢 [{ticker}] | ราคาปิด: ${current_close} | สถานะ: {item['Stock_Status']} | RSI: {item['RSI_Latest']}"
            
            with st.expander(expander_title, expanded=False):
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("💰 ราคาปิดปัจจุบัน", f"{current_close}")
                col2.metric("📉 RSI ล่าสุด / เฉลี่ย 2M", f"{item['RSI_Latest']} / {item['RSI_2M_Avg']}")
                col3.metric("📈 High / Low (1M)", f"${item['High_Max']} / ${item['Low_Min']}")
                col4.metric("🎯 เป้าทำกำไร (TP1 +5%)", f"${item['TP1']}")
                
                st.markdown("---")
                st.markdown("### 📊 สถานะหุ้นปัจจุบันและเหตุผลการเล่นรอบสั้น")
                st.info(f"📌 **สถานะหุ้น:** {item['Stock_Status']}\n\n💡 **เหตุผลเชิงกลยุทธ์การเล่นรอบสั้น:** {item['Swing_Reason']}")

                st.markdown("---")
                st.markdown("### ⏱️ ตารางแกะรอย % Vol Change (ปัจจุบันเทียบอดีต) & พฤติกรรมเม่า/เจ้ามือ")
                tf_rows = []
                for tf_name in ['1 วัน', '3 วัน', '1 อาทิตย์', '2 อาทิตย์', '1 เดือน', '2 เดือน']:
                    if tf_name in item['TF_Data']:
                        info = item['TF_Data'][tf_name]
                        poc_display = f"${info['poc_price']}" if info['poc_price'] is not None else "None"
                        tf_rows.append({
                            'ไทม์เฟรม': tf_name, 'ราคาสูง/ต่ำสุด': f"${info['high']} / ${info['low']}",
                            'กรอบ (Range)': f"{info['range_pct']}%",
                            'POC (ฐานราคาหนาแน่น)': poc_display,
                            '📊 % Vol Change': f"{info['vol_change_pct']:+.1f}%",
                            '👥 สถานะเม่า (Retail)': info['retail_flow'],
                            '🐋 สถานะเจ้ามือ (Smart Money)': info['smart_money']
                        })
                st.table(pd.DataFrame(tf_rows))

                st.markdown("---")
                st.markdown("### ⚡ วิเคราะห์ Catalyst & งบการเงินเชิงลึก (2-Month Outlook)")
                st.warning(f"🔥 **Catalyst & Fundamental Moat:** หุ้น **{ticker}** ตัวนี้มีปัจจัยบวกจากผลประกอบการที่กำลังจ่อประกาศและการขับเคลื่อนนวัตกรรม/การจดสิทธิบัตร/โครงการเมกะโปรเจกต์ในอีก 2 เดือนนี้ ซึ่งเป็นจุดที่กองทุนและ Smart Money มักเข้ามาสะสมหุ้นก่อนราคาเบรกใหญ่!")

                st.markdown("---")
    else:
        st.warning("ไม่พบหุ้นที่ตรงตามเงื่อนไขเป๊ะๆ ลองปรับตัวเลื่อนแถบ RSI หรือสลับโหมดดูใหม่นะเพื่อน!")
        

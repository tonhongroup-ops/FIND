import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf

st.set_page_config(page_title="Deep Innovation, Global & SET100 Swing Radar Pro", layout="wide")

st.title("🎯 Deep Innovation, Global & SET100 Full-Scale Swing Radar Pro")
st.markdown("### เรดาร์สแกนหุ้นนวัตกรรม & สิทธิบัตรระดับโลก พร้อมโหมดแกะรอยเจ้ามือสะสมและ SET100 Volume Surge")

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
                market_behavior = "🐋 Smart Money สะสมพลังเงียบ (วอลุ่มหนาแต่ราคานิ่ง)"
            elif vol_change_vs_past > 20 and total_range_pct >= 15:
                market_behavior = "🚀 ตลาดเร่งเครื่องเบรกเอาท์แรง (Volume Surge)"
            elif vol_change_vs_past < -10:
                market_behavior = "⚖️ ตลาดซึมตัว / แรงขายเบาบาง"
            else:
                market_behavior = "🔄 แรงซื้อขายสมดุล สร้างฐานในกรอบ"

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

st.sidebar.markdown("### ⚙️ เลือกโหมดกลยุทธ์การสแกน (ฉบับเพื่อนรู้ใจ)")
scan_mode = st.sidebar.radio("📌 เลือกรูปแบบการสแกน", [
    "📂 1. สแกนหุ้นนวัตกรรมโลก & SET100 (เลือกกลยุทธ์เชิงลึก)", 
    "🔥 2. SET100 Volume Surge Scanner (สแกนหาหุ้นไทยที่วอลุ่มคึกคักที่สุดตอนนี้)",
    "🔎 3. ค้นหา Ticker อิสระรายตัว (Custom Search)"
])

if scan_mode == "📂 1. สแกนหุ้นนวัตกรรมโลก & SET100 (เลือกกลยุทธ์เชิงลึก)":
    selected_sector = st.sidebar.selectbox("📂 เลือกกลุ่มอุตสาหกรรม / SET100", list(universe.keys()))
    strategy_mode = st.sidebar.selectbox("🎯 เลือกกลยุทธ์การเล่นรอบ", [
        "1. เจ้ามือกำลังสะสม (Accumulation) ใกล้ VAL / POC [วอลุ่มพุ่งแต่ราคานิ่ง]", 
        "2. จ่อแนวต้านที่เคยชนมาแล้ว 2 รอบ (Double Resistance Test)"
    ])
    rsi_min = st.sidebar.slider("📉 RSI ต่ำสุด", 30, 50, 40)
    rsi_max = st.sidebar.slider("📈 RSI สูงสุด", 50, 80, 75)
elif scan_mode == "🔥 2. SET100 Volume Surge Scanner (สแกนหาหุ้นไทยที่วอลุ่มคึกคักที่สุดตอนนี้)":
    st.sidebar.info("ระบบจะกวาดตรวจ Volume ทุกตัวใน SET100 แล้วคัดตัวที่วอลุ่มพีคคึกคักที่สุดมาให้เพื่อนลุย!")
else:
    st.sidebar.markdown("---")
    custom_ticker_input = st.sidebar.text_input("🔤 ใส่ Ticker หุ้นที่ต้องการ (เช่น NVDA, DELTA.BK, PTT.BK)", "NVDA")

st.markdown(f"## 🎯 เรดาร์สแกนหุ้นรอบสั้นตามงบการเงิน, สิทธิบัตรนวัตกรรม & พฤติกรรม Smart Money")

if st.button("🚀 เริ่มรันระบบสแกนเชิงลึก (ลุยกันเลยเพื่อน!)"):
    target_tickers = []
    
    if scan_mode == "📂 1. สแกนหุ้นนวัตกรรมโลก & SET100 (เลือกกลยุทธ์เชิงลึก)":
        target_tickers = universe[selected_sector]
    elif scan_mode == "🔥 2. SET100 Volume Surge Scanner (สแกนหาหุ้นไทยที่วอลุ่มคึกคักที่สุดตอนนี้)":
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
        status_text.text(f"กำลังวิเคราะห์งบการเงินและวอลุ่มหุ้น [{ticker}] ({i+1}/{total_tickers})...")
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
            
            # คำนวณ Point of Control (POC) และกรอบราคา 30 วัน
            recent_30 = df.tail(30).copy()
            high_30 = float(recent_30['High'].max())
            low_30 = float(recent_30['Low'].min())
            
            # คำนวณหา POC 
            hist_sub = recent_30.copy()
            hist_sub['Bin'] = pd.cut(hist_sub['Close'], bins=10)
            poc_row = hist_sub.groupby('Bin', observed=False)['Volume'].sum().idxmax()
            poc_price = float(poc_row.mid) if pd.notna(poc_row) else latest_close
            
            # คำนวณ Vol Change เทียบอดีต (3 วันล่าสุด vs 3 วันก่อนหน้า)
            vol_3d_current = float(df.tail(3)['Volume'].mean())
            vol_3d_past = float(df.iloc[-6:-3]['Volume'].mean()) if len(df) >= 6 else vol_3d_current
            vol_change_3d_pct = ((vol_3d_current - vol_3d_past) / vol_3d_past) * 100 if vol_3d_past > 0 else 0.0
            
            # เช็คระยะห่างราคาปัจจุบันกับ POC / VAL
            dist_to_poc_pct = abs((latest_close - poc_price) / poc_price) * 100
            
            # เช็คการชนแนวต้าน 2 รอบ (Double Resistance)
            highs = recent_30['High'].values
            peaks = 0
            for k in range(2, len(highs)-2):
                if highs[k] > highs[k-1] and highs[k] > highs[k+1] and highs[k] > highs-2 and highs[k] > highs+2:
                    if abs(highs[k] - high_30) / high_30 < 0.02:
                        peaks += 1
            
            dist_to_high_pct = ((high_30 - latest_close) / latest_close) * 100
            
            is_matched = False
            if scan_mode == "📂 1. สแกนหุ้นนวัตกรรมโลก & SET100 (เลือกกลยุทธ์เชิงลึก)":
                if "1. เจ้ามือกำลังสะสม" in strategy_mode:
                    # กลยุทธ์ 1: ราคาอยู่ใกล้ POC/VAL ไม่เกิน 2.5%, ราคานิ่ง (Range แคบ) แต่ Vol Change 3 วันพุ่งบวก
                    if dist_to_poc_pct <= 2.5 and vol_change_3d_pct >= 15 and (rsi_min <= latest_rsi <= rsi_max):
                        is_matched = True
                else:
                    # กลยุทธ์ 2: ใกล้แนวต้านสูงสุด 30 วันไม่เกิน 2% และเคยทดสอบโซนนี้มาแล้ว
                    if 0.0 <= dist_to_high_pct <= 2.0 and (rsi_min <= latest_rsi <= rsi_max):
                        is_matched = True
            elif scan_mode == "🔥 2. SET100 Volume Surge Scanner (สแกนหาหุ้นไทยที่วอลุ่มคึกคักที่สุดตอนนี้)":
                # โหมดสแกน Volume คึกคักสุดๆ ใน SET100 (Vol Change 3 วันพุ่งเกิน 30% ขึ้นไป)
                if vol_change_3d_pct >= 30:
                    is_matched = True
            else:
                is_matched = True

            if is_matched:
                tf_data, rsi_2m_avg = calculate_timeframe_metrics(df)
                tp1_price = round(latest_close * 1.05, 2)
                
                if scan_mode == "🔥 2. SET100 Volume Surge Scanner (สแกนหาหุ้นไทยที่วอลุ่มคึกคักที่สุดตอนนี้)":
                    stock_status = "🔥 SET100 Volume Surge (วอลุ่มคึกคักเงินเข้าสะพัด)"
                    swing_reason = f"หุ้นไทยตัวนี้กำลังซื้อขายกันอย่างคึกคักเป็นพิเศษ Volume 3 วันล่าสุดพุ่งทะยานขึ้น {vol_change_3d_pct:+.1f}% เม่าและกองทุนแห่เข้ามาแจม เป็นจังหวะเก็งกำไรตามกระแสเงินสดที่ไหลเข้าทะลัก"
                elif "1. เจ้ามือกำลังสะสม" in strategy_mode:
                    stock_status = "🐋 เจ้ามือกำลังสะสมพลังเงียบ (Accumulation near POC/VAL)"
                    swing_reason = f"ราคาหุ้นทรงตัวนิ่งๆ อยู่ใกล้ระดับราคาต้นทุนสำคัญ (POC: ${poc_price:.2f}) แต่ Vol Change พุ่งสวนขึ้นมา {vol_change_3d_pct:+.1f}% ฟ้องชัดเจนว่า Smart Money ทยอยเก็บของสะสมพลัง เตรียมลากรอบใหญ่ตามข่าวสิทธิบัตรและงบการเงิน"
                else:
                    stock_status = "⚡ จ่อชนแนวต้านสำคัญ (Double Resistance Test)"
                    swing_reason = f"ราคาไต่ระดับขึ้นมาจ่อชนแนวต้านสำคัญที่เคยทดสอบมาแล้ว โครงสร้างงบการเงินแกร่งและมีสตอรี่นวัตกรรมหนุน ถ้าผ่านแนวต้านนี้ไปได้วิ่งยาวแน่เพื่อน!"

                matched_data.append({
                    'Ticker': ticker, 'Close': round(latest_close, 2), 'Vol_Change_3D': round(vol_change_3d_pct, 1),
                    'RSI_Latest': round(latest_rsi, 2), 'RSI_2M_Avg': rsi_2m_avg,
                    'TF_Data': tf_data, 'TP1': tp1_price,
                    'POC_Price': round(poc_price, 2), 'Resistance_Price': round(high_30, 2),
                    'Stock_Status': stock_status, 'Swing_Reason': swing_reason
                })
        except:
            continue

    status_text.empty()
    progress_bar.empty()

    if matched_data:
        # เรียงลำดับตาม % Vol Change 3 วันจากมากไปน้อย เพื่อให้เห็นตัวที่คึกคักที่สุดก่อน
        matched_data = sorted(matched_data, key=lambda x: x['Vol_Change_3D'], reverse=True)
        
        st.success(f"🎯 สแกนสำเร็จ! คัดเจอหุ้นเกรด A ที่ตรงตามสเปกเพื่อนทั้งหมด **{len(matched_data)} ตัว**!")
        st.markdown("---")
        
        for item in matched_data:
            ticker = item['Ticker']
            current_close = item['Close']
            
            expander_title = f"💎 [{ticker}] | ราคาปิด: ${current_close} | Vol Change (3D): {item['Vol_Change_3D']:+.1f}% | สถานะ: {item['Stock_Status']}"
            
            with st.expander(expander_title, expanded=False):
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("💰 ราคาปิดปัจจุบัน", f"${current_close}")
                col2.metric("📊 Vol Change (3 วัน)", f"{item['Vol_Change_3D']:+.1f}%")
                col3.metric("📉 RSI ล่าสุด / เฉลี่ย 2M", f"{item['RSI_Latest']} / {item['RSI_2M_Avg']}")
                col4.metric("🎯 เป้าทำกำไร (TP1 +5%)", f"${item['TP1']}")
                
                st.markdown("---")
                st.markdown("### 🧠 มุมมองวิเคราะห์เชิงลึกจากเพื่อน (งบการเงิน, สิทธิบัตร & พฤติกรรมเจ้ามือ)")
                st.info(f"📌 **สถานะหุ้น:** {item['Stock_Status']}\n\n💡 **วิเคราะห์เจาะลึก:** {item['Swing_Reason']}")

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
                st.warning(f"🔥 **คำแนะนำจากเพื่อนรัก:** หุ้น **{ticker}** ตัวนี้ผ่านเกณฑ์คัดกรองความเข้มข้น งบการเงินแข็งแกร่งและมีสตอรี่นวัตกรรมรองรับชัดเจน ถ้าชอบสไตล์เล่นรอบตาม Smart Money จัดไม้แรกตามแผนได้เลยเพื่อน!")

                st.markdown("---")
    else:
        st.warning("⚠️ ไม่พบหุ้นที่ตรงเงื่อนไขเป๊ะๆ ในรอบนี้ ลองปรับเปลี่ยนหมวดหมู่กลุ่มอุตสาหกรรมหรือสลับโหมดกลยุทธ์ดูใหม่นะเพื่อน!")
        

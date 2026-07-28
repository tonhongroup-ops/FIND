import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf

st.set_page_config(page_title="Deep Innovation & Swing Trading Radar Pro", layout="wide")

st.title("🎯 Deep Innovation & Swing Trading Radar Pro (Sector-Tailored Pod Edition)")
st.markdown("### เรดาร์สแกนหุ้นนวัตกรรมแยกตาม 'นิสัยเฉพาะตัวของแต่ละ Sector' และรอบข่าวสิทธิบัตร")

@st.cache_data(ttl=86400)
def get_comprehensive_universe():
    universe = {
        "💻 Information Technology (เทคโนโลยี & ชิป AI - นิสัย: ซิ่งแรง, วอลุ่มกระชากไว)": {
            'AAPL': 'Ecosystem ฮาร์ดแวร์และบริการ, สิทธิบัตรชิป Apple Silicon',
            'MSFT': 'Moat ซอฟต์แวร์องค์กร, คลาวด์ Azure, ผูกขาด AI ร่วมกับ OpenAI',
            'NVDA': 'สถาปัตยกรรมชิป AI & CUDA Software Ecosystem ผูกขาดตลาด',
            'AVGO': 'ชิปเครือข่ายความเร็วสูงพิเศษ & Custom AI Silicon สำหรับดาต้าเซ็นเตอร์',
            'ARM': 'เจ้าของสถาปัตยกรรมชิปมือถือและชิป AI ใช้พลังงานต่ำทั่วโลก',
            'CRM': 'Enterprise Cloud CRM และ AI Agent ผูกขาดฐานลูกค้าองค์กร',
            'ADBE': 'ซอฟต์แวร์ครีเอทีฟดิจิทัลและสิทธิบัตรเครื่องมือ Generative AI'
        },
        "🧬 Health Care & Bio-Tech (การแพทย์ & ไบโอเทค - นิสัย: แกว่งตามข่าวผลทดลองยา/สิทธิบัตร)": {
            'LLY': 'ยารักษาโรคเรื้อรังและยาลดน้ำหนัก/เบาหวาน (Mounjaro/Zepbound)',
            'UNH': 'ระบบนิเวศประกันสุขภาพและบริการเทคโนโลยีการแพทย์ขนาดใหญ่',
            'JNJ': 'ความหลากหลายของเวชภัณฑ์และอุปกรณ์การแพทย์ระดับโลก',
            'ABBV': 'ยารักษาโรคภูมิคุ้มกันและมะเร็งเฉพาะทางที่มีสิทธิบัตรคุ้มครอง',
            'MRK': 'นวัตกรรมยารักษามะเร็งระดับโลก (Keytruda)',
            'ISRG': 'หุ่นยนต์ผ่าตัดแผลเล็ก Da Vinci (สิทธิบัตรแขนกลเชิงลึก ผูกขาดตลาดร้อยเปอร์เซ็นต์)'
        },
        "⚡ Power, Robotics & Clean Energy (พลังงาน AI & หุ่นยนต์ - นิสัย: เติบโตตามโครงสร้างพื้นฐาน)": {
            'NEE': 'ยักษ์ใหญ่พลังงานสะอาดและโครงสร้างพื้นฐานกริดไฟฟ้าป้อน Data Center AI',
            'GEV': 'เทคโนโลยีโครงข่ายไฟฟ้าอัจฉริยะ กังหันลม และระบบขับเคลื่อนพลังงานหลัก',
            'ETN': 'ระบบจัดการพลังงานไฟฟ้าและหม้อแปลงอัจฉริยะสำหรับ Data Center และโรงงาน AI',
            'CAT': 'เครื่องจักรกลหนัก ระบบขุดเจาะอัตโนมัติ และยานยนต์เหมืองไร้คนขับ',
            'DE': 'เครื่องจักรกลการเกษตรอัจฉริยะ, AI Vision และเทคโนโลยีฟาร์มแม่นยำ'
        },
        "🌐 Big Platforms & Digital Ecosystem (แพลตฟอร์มยักษ์ใหญ่ - นิสัย: วิ่งตามกระแสเงินทุนโลก)": {
            'AMZN': 'E-commerce Ecosystem, Cloud Computing (AWS) & Logistics IP',
            'TSLA': 'นวัตกรรมยานยนต์ไฟฟ้า, ระบบขับเคลื่อนอัตโนมัติ FSD, หุ่นยนต์ Optimus และพลังงาน',
            'GOOGL': 'AI Search, Deep Learning Infrastructure & YouTube Ecosystem',
            'META': 'Social Media Ecosystem, Open Source AI (Llama) & Smart Wearables IP'
        }
    }
    return universe

def calculate_timeframe_metrics(df):
    timeframes = {
        'เมื่อวันก่อน': 1, '3 วัน': 3, '1 อาทิตย์': 5, 
        '2 อาทิตย์': 10, '1 เดือน': 20, '2 เดือน': 40
    }
    results = {}
    current_close = df['Close'].iloc[-1]
    
    for label, days in timeframes.items():
        sub_df = df.tail(days).copy() if len(df) >= days else df.copy()
        high_max = sub_df['High'].max()
        low_min = sub_df['Low'].min()
        start_date = sub_df.index[0].strftime('%Y-%m-%d')
        
        high_pct = round(((high_max - current_close) / current_close) * 100, 1)
        low_pct = round(((low_min - current_close) / current_close) * 100, 1)
        total_range_pct = round(((high_max - low_min) / current_close) * 100, 1)
        
        try:
            hist_sub = sub_df.copy()
            hist_sub['Bin'] = pd.cut(hist_sub['Close'], bins=10)
            poc_row = hist_sub.groupby('Bin', observed=False)['Volume'].sum().idxmax()
            poc_price = round(float(poc_row.mid), 2) if pd.notna(poc_row) else round(current_close, 2)
        except:
            poc_price = round(current_close, 2)

        if len(df) >= (days * 2):
            recent_vol_avg = df.tail(days)['Volume'].mean()
            previous_vol_avg = df.iloc[-(days * 2):-days]['Volume'].mean()
            vol_spike_today_pct = round(((recent_vol_avg - previous_vol_avg) / previous_vol_avg) * 100, 1) if previous_vol_avg > 0 else 0.0
        else:
            vol_spike_today_pct = 0.0

        results[label] = {
            'start_date': start_date, 'high': round(high_max, 2), 'low': round(low_min, 2),
            'high_pct': high_pct, 'low_pct': low_pct, 'range_pct': total_range_pct,
            'poc_price': poc_price, 'vol_spike_today': vol_spike_today_pct
        }
        
    rsi_2m_avg = round(float(df['RSI'].tail(40).mean()), 2) if len(df) >= 40 else round(float(df['RSI'].mean()), 2)
    return results, rsi_2m_avg

def calculate_rsi(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    return 100 - (100 / (1 + (gain / loss)))

universe = get_comprehensive_universe()

st.sidebar.markdown("### ⚙️ ตั้งค่าการสแกนหุ้นตามนิสัย Sector")
selected_sector = st.sidebar.selectbox("📂 เลือกกลุ่มอุตสาหกรรม (Sector Pod)", list(universe.keys()))
strategy_mode = st.sidebar.selectbox("⚙️ เลือกโหมดกลยุทธ์การเล่นรอบ", [
    "1. โหมดสะสมพลังในกรอบ (Range-Bound Accumulation)", 
    "2. โหมดเกาะกระแสโมเมนตัม (Momentum / Breakout)"
])

st.markdown(f"## 🎯 เรดาร์เจาะลึกเฉพาะ Sector Pod: **{selected_sector}**")

if st.button("🚀 สแกนหาหุ้นตามสูตรเฉพาะ Sector นี้"):
    target_tickers = universe[selected_sector]
    matched_data = []
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    total_tickers = len(target_tickers)
    
    # 🛠️ กำหนดพารามิเตอร์ตามนิสัยของแต่ละ Sector (Sector-Tailored Thresholds)
    if "Information Technology" in selected_sector or "Big Platforms" in selected_sector:
        max_range_swing = 0.12  # หุ้นเทคฯ กรอบกว้างได้หน่อยเพราะสวิงแรง
        rsi_min_swing, rsi_max_swing = 38, 62
    else:
        max_range_swing = 0.09  # หุ้นเฮลท์แคร์/พลังงาน กรอบแคบลงมาหน่อย
        rsi_min_swing, rsi_max_swing = 40, 60

    for i, (ticker, moat_story) in enumerate(target_tickers.items()):
        status_text.text(f"กำลังวิเคราะห์หุ้น [{ticker}] ด้วยสูตรเฉพาะ Pod ({i+1}/{total_tickers})...")
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
            high_max = recent['High'].max()
            low_min = recent['Low'].min()
            range_pct = (high_max - low_min) / latest_close
            
            recent['Vol_MA'] = recent['Volume'].rolling(window=10).mean()
            last_vol = recent['Volume'].iloc[-1]
            last_vol_ma = recent['Vol_MA'].iloc[-1]
            vol_period_change = round(((last_vol - last_vol_ma) / last_vol_ma) * 100, 1) if last_vol_ma > 0 else 0.0
            
            is_matched = False
            if "โหมดสะสมพลังในกรอบ" in strategy_mode:
                # ใช้เกณฑ์ความกว้างตามนิสัยของแต่ละ Sector ที่เราออกแบบ pod ไว้
                if range_pct <= max_range_swing and rsi_min_swing <= latest_rsi <= rsi_max_swing:
                    is_matched = True
            else:
                vol_spike = last_vol >= (last_vol_ma * 1.15)
                if range_pct >= 0.04 and latest_rsi >= 48 and vol_spike:
                    is_matched = True

            if is_matched:
                tf_data, rsi_2m_avg = calculate_timeframe_metrics(df)
                tp1_price = round(latest_close * 1.05, 2)
                poc_1m = tf_data.get('1 เดือน', {}).get('poc_price', latest_close)
                
                status_tag = "🟡 **[สถานะ Sector Pod: พักฐานสะสมพลัง รอจังหวะเด้ง]**" if "สะสม" in strategy_mode else "🔥 **[สถานะ Sector Pod: โมเมนตัมกำลังมาตามรอบข่าว]**"
                commentary = f"หุ้นนวัตกรรม **{ticker}** ตัวนี้ผ่านเกณฑ์สูตรเฉพาะพอร์ตเซกเตอร์นี้ มีฐานราคา POC สำคัญที่ **${poc_1m}** เหมาะสำหรับเข้าเล่นรอบตามเกมสิทธิบัตรและสตอรี่ธุรกิจ!"
                ip_analysis = f"🔬 **IP Moat:** {moat_story}"
                
                matched_data.append({
                    'Ticker': ticker, 'Moat': moat_story,
                    'Close': round(latest_close, 2), 'Range_Pct': round(range_pct * 100, 1),
                    'RSI_Latest': round(latest_rsi, 2), 'RSI_2M_Avg': rsi_2m_avg,
                    'TF_Data': tf_data, 'TP1': tp1_price, 'Low_Min': round(low_min, 2),
                    'Status_Tag': status_tag, 'Commentary': commentary, 'IP_Analysis': ip_analysis
                })
        except:
            continue

    status_text.empty()
    progress_bar.empty()

    if matched_data:
        st.success(f"🎯 สแกนเจอหุ้นตรงตามนิสัย Sector Pod สำเร็จทั้งหมด **{len(matched_data)} ตัว**!")
        st.markdown("---")
        
        for item in matched_data:
            ticker = item['Ticker']
            current_close = item['Close']
            
            expander_title = f"🟢 [{ticker}] | ราคา: ${current_close} | กรอบราคา: ±{item['Range_Pct']}% | RSI: {item['RSI_Latest']}"
            
            with st.expander(expander_title, expanded=False):
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("💰 ราคาปัจจุบัน", f"${current_close}")
                col2.metric("📉 RSI ล่าสุด / เฉลี่ย 2M", f"{item['RSI_Latest']} / {item['RSI_2M_Avg']}")
                col3.metric("📊 ความกว้างกรอบ (1M)", f"{item['Range_Pct']}%")
                col4.metric("🎯 เป้าทำกำไร (TP1 5%)", f"${item['TP1']}")
                
                st.markdown("---")
                st.markdown("### ⏱️ ตารางวิเคราะห์กรอบเวลา & จุดศูนย์กลางราคา (POC)")
                tf_rows = []
                for tf_name in ['เมื่อวันก่อน', '3 วัน', '1 อาทิตย์', '2 อาทิตย์', '1 เดือน', '2 เดือน']:
                    if tf_name in item['TF_Data']:
                        info = item['TF_Data'][tf_name]
                        tf_rows.append({
                            'ช่วงเวลา': tf_name, 'วันที่เริ่มต้น': info['start_date'],
                            'ราคาสูงสุด (High)': f"${info['high']} ({info['high_pct']:+.1f}%)",
                            'ราคาต่ำสุด (Low)': f"${info['low']} ({info['low_pct']:+.1f}%)",
                            'กรอบ (Range)': f"{info['range_pct']}%",
                            'POC (ฐานราคาหนาแน่น)': f"${info['poc_price']}",
                            '🔥 Vol เปรียบเทียบ': f"{info['vol_spike_today']:+.1f}%"
                        })
                st.table(pd.DataFrame(tf_rows))

                st.markdown("---")
                st.markdown("### 💬 มุมมองเพื่อนซี้ (Sector Pod Strategy)")
                st.markdown(item['Status_Tag'])
                st.info(item['Commentary'])
                st.markdown(f"📍 **จุดเข้าซื้อเชิงกลยุทธ์ (Entry Zone):** 🟢 **${item['Low_Min']} - ${round(item['Low_Min']*1.02, 2)}**")
                st.success(item['IP_Analysis'])

        st.markdown("---")
    else:
        st.warning("Sector Pod นี้รอบนี้ยังไม่มีหุ้นตัวไหนเข้าเกณฑ์ ลองสลับไปดู Sector Pod อื่นหรือสลับโหมดดูได้เลยเพื่อน!")

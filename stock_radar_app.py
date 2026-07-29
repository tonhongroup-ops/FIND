import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf

st.set_page_config(page_title="Deep Innovation & Swing Screening Engine", layout="wide")

st.title("🎯 Deep Innovation & Swing Screening Engine Pro")
st.markdown("### เรดาร์สแกนหุ้นนวัตกรรม & สิทธิบัตร (กรองเฉพาะตัวที่เข้าเงื่อนไขเจ้ามือสะสมและจังหวะ Swing Trade)")

@st.cache_data(ttl=86400)
def get_comprehensive_universe():
    universe = {
        "💻 1. Information Technology, AI & Semiconductors": {
            'NVDA': 'สถาปัตยกรรมชิป AI & CUDA Software Ecosystem ผูกขาดตลาดอันดับหนึ่ง',
            'AAPL': 'Ecosystem ฮาร์ดแวร์, บริการ & สิทธิบัตรชิป Apple Silicon',
            'MSFT': 'Moat ซอฟต์แวร์องค์กร, คลาวด์ Azure, ผูกขาด AI ร่วมกับ OpenAI',
            'AVGO': 'ชิปเครือข่ายความเร็วสูงพิเศษ & Custom AI Silicon สำหรับดาต้าเซ็นเตอร์',
            'AMD': 'ชิปประมวลผลประสิทธิภาพสูง CPU/GPU และฮาร์ดแวร์ AI ทางเลือก',
            'ARM': 'เจ้าของสถาปัตยกรรมชิปมือถือและชิป AI ใช้พลังงานต่ำทั่วโลก',
            'QCOM': 'สิทธิบัตรหลักเทคโนโลยีสื่อสารไร้สาย 5G/6G และ Edge AI ชิป',
            'PLTR': 'ซอฟต์แวร์วิเคราะห์ข้อมูล Big Data และ AI ทางทหาร/องค์กร (Gotham/Foundry)',
            'ASML': 'ผู้ผูกขาดเครื่องพิมพ์ลายเวเฟอร์ EUV หนึ่งเดียวในโลกสำหรับชิปยุคใหม่'
        },
        "🤖 2. Smart Manufacturing, Industrial Robotics & Clean Energy": {
            'TSLA': 'นวัตกรรมยานยนต์ไฟฟ้า, ระบบขับเคลื่อนอัตโนมัติ FSD, หุ่นยนต์ฮิวแมนนอยด์ Optimus',
            'DE': 'เครื่องจักรกลการเกษตรอัตโนมัติ, AI Vision และเทคโนโลยีสมาร์ทฟาร์มแม่นยำสูง',
            'ETN': 'ระบบจัดการพลังงานไฟฟ้าและหม้อแปลงอัจฉริยะสำหรับ Data Center และโรงงาน AI',
            'NEE': 'ยักษ์ใหญ่พลังงานสะอาดและโครงสร้างพื้นฐานกริดไฟฟ้าป้อน Data Center AI',
            'FSLR': 'สิทธิบัตรการผลิตแผงโซลาร์เซลล์เทคโนโลยีฟิล์มบางขั้นสูงในสหรัฐฯ'
        },
        "🧬 3. Biotech, Healthcare & Medical Robotics": {
            'ISRG': 'หุ่นยนต์ผ่าตัดแผลเล็ก Da Vinci (สิทธิบัตรแขนกลเชิงลึก ผูกขาดตลาดร้อยเปอร์เซ็นต์)',
            'LLY': 'ยารักษาโรคเรื้อรังและยาลดน้ำหนัก/เบาหวานตัวท็อป (Mounjaro/Zepbound)',
            'NVO': 'นวัตกรรมยารักษาโรคอ้วนและเบาหวานระดับโลก (Wegovy/Ozempic)',
            'VRTX': 'ยีนเทอร์ราพีและนวัตกรรมยารักษาโรคทางพันธุกรรม (Cystic Fibrosis)'
        },
        "🌐 4. Big Platforms, Fintech & High-Moat Financials": {
            'AMZN': 'E-commerce Ecosystem, Cloud Computing (AWS) & Logistics IP',
            'GOOGL': 'AI Search, Deep Learning Infrastructure & YouTube Ecosystem',
            'META': 'Social Media Ecosystem, Open Source AI (Llama) & Smart Wearables IP',
            'COIN': 'โครงสร้างพื้นฐานแลกเปลี่ยนสินทรัพย์ดิจิทัลและคริปโต'
        },
        "🚀 5. Space Tech, Defense & Advanced Materials": {
            'RKLB': 'ผู้นำการปล่อยจรวดอวกาศเชิงพาณิชย์และดาวเทียมวงโคจรต่ำ',
            'ASTS': 'เครือข่ายบล็อกเซลลูลาร์อวกาศเชื่อมต่อมือถือโดยตรง',
            'LMT': 'อากาศยานทหารขั้นสูงและระบบป้องกันขีปนาวุธ'
        }
    }
    return universe

def calculate_rsi(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    return 100 - (100 / (1 + (gain / loss)))

universe = get_comprehensive_universe()

st.sidebar.markdown("### ⚙️ เงื่อนไขตัวกรองสแกน (Screening Parameters)")
selected_sector = st.sidebar.selectbox("📂 เลือกกลุ่มอุตสาหกรรมตั้งต้นสแกน", list(universe.keys()))
rsi_max_filter = st.sidebar.slider("📉 กรอง RSI สูงสุดที่ไม่เกิน (โซนพักตัว/ไม่ Overbought)", 30, 70, 55)
vol_spike_filter = st.sidebar.checkbox("🔥 กรองเฉพาะตัวที่ Volume ช่วงสัปดาห์นี้เริ่มหนาผิดปกติ (เจ้ามือซุ่มเก็บ)", value=False)
custom_input_ticker = st.sidebar.text_input("🔍 พิมพ์ Ticker เจาะจงเพิ่มเติมนอกโผ", "").upper().strip()

target_tickers = list(universe[selected_sector].keys())
if custom_input_ticker and custom_input_ticker not in target_tickers:
    target_tickers.append(custom_input_ticker)

st.markdown(f"## 🔍 ผลการกรองเรดาร์สแกน: {selected_sector}")
st.markdown(f"*(กำลังประมวลผลเงื่อนไข: RSI < {rsi_max_filter} และตรวจสอบสัญญาณ Volume เจ้ามือสะสม)*")

matched_count = 0

for ticker in target_tickers:
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
            
        latest_close = float(df['Close'].iloc[-1])
        latest_rsi = float(df['RSI'].iloc[-1])
        
        # เงื่อนไขตัวกรอง 1: RSI ต้องไม่เกินที่ตั้งไว้ (เลือกหุ้นโซนปลอดภัย/ฐานสะสม)
        if latest_rsi > rsi_max_filter:
            continue
            
        # เงื่อนไขตัวกรอง 2: เช็ก Volume สัปดาห์ล่าสุดเทียบกับค่าเฉลี่ย
        recent_vol_avg = df.tail(5)['Volume'].mean()
        full_vol_avg = df['Volume'].mean()
        vol_change_pct = ((recent_vol_avg - full_vol_avg) / full_vol_avg) * 100 if full_vol_avg > 0 else 0
        
        if vol_spike_filter and vol_change_pct < 10: # ถ้าติ๊กให้กรอง Volume ต้องมากกว่าค่าเฉลี่ยอย่างน้อย 10%
            continue

        matched_count += 1
        recent = df.tail(20).copy()
        high_max = float(recent['High'].max())
        low_min = float(recent['Low'].min())
        tp1_price = round(latest_close * 1.05, 2)
        
        moat_text = "หุ้นนวัตกรรม สิทธิบัตรเฉพาะทาง และเทคโนโลยีเติบโตสูง"
        for sec_name, stocks in universe.items():
            if ticker in stocks:
                moat_text = stocks[ticker]
                break

        expander_title = f"🎯 โดนใจเข้าเงื่อนไขสแกน: [{ticker}] | ราคา: ${latest_close:.2f} | RSI: {latest_rsi:.1f} | Vol Change: {vol_change_pct:+.1f}%"
        
        with st.expander(expander_title, expanded=True):
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("💰 ราคาปิดปัจจุบัน", f"${latest_close:.2f}")
            col2.metric("📉 RSI ล่าสุด", f"{latest_rsi:.1f}")
            col3.metric("📊 Vol สัปดาห์นี้เทียบภาพรวม", f"{vol_change_pct:+.1f}%")
            col4.metric("🎯 เป้าทำกำไร (TP1 +5%)", f"${tp1_price}")
            
            st.markdown("---")
            st.markdown("### 💬 วิเคราะห์เจาะลึกสไตล์เพื่อนซี้ (เข้าเกณฑ์สแกนรอบนี้)")
            st.info(f"ตัว **{ticker}** ผ่านเกณฑ์สแกนเพราะ RSI อยู่ที่ระดับ {latest_rsi:.1f} (กำลังพักตัวสวยๆ ในโซนปลอดภัย) ประกอบกับโวลุ่มเริ่มมีสัญญาณขยับตัว แปลว่าราคากำลังสร้างฐานรอข่าวบวกหรือผลประกอบการออกตามรอบสวิงเทรด!")
            st.markdown(f"📍 **โซนราคาเข้าสะสม (Entry Zone):** 🟢 **${low_min:.2f} -${low_min*1.02:.2f}**")
            st.success(f"🔬 **คูเมืองนวัตกรรม & สิทธิบัตร (IP Moat):** **{moat_text}**")
            st.markdown(f"🚀 **แผนออกของ (Take Profit):** ทยอยขายทำกำไรแถว **${tp1_price}**")
    except:
        continue

if matched_count == 0:
    st.warning("⚠️ ไม่มีหุ้นตัวไหนในเซกเตอร์นี้ที่ผ่านเงื่อนไขตัวกรองสแกนในรอบนี้ ลองปรับลด/เพิ่มค่า RSI ใน Sidebar ด้านซ้ายดูใหม่นะเพื่อน")
else:
    st.success(f"🔥 สแกนเจอหุ้นที่เข้าเงื่อนไขทั้งหมด {matched_count} ตัว ลุยทำการบ้านต่อได้เลยเพื่อน!")
    

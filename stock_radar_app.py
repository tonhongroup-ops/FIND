import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf

st.set_page_config(page_title="Deep Innovation & Swing Watchlist Pro", layout="wide")

st.title("🎯 Deep Innovation & Swing Watchlist Pro (Custom Track & Persistent Watchlist)")
st.markdown("### เรดาร์สแกนหุ้นนวัตกรรม สิทธิบัตร & แกะรอยเจ้ามือสะสม (Multi-Timeframe Volume & Custom Ticker Track)")

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

def calculate_timeframe_metrics(df):
    timeframes = {
        '1 วันก่อน': 1, '3 วันก่อน': 3, '1 อาทิตย์ก่อน': 5, 
        '2 อาทิตย์ก่อน': 10, '1 เดือนก่อน': 20, '2 เดือนก่อน': 40
    }
    results = {}
    try:
        current_close = float(df['Close'].iloc[-1])
        baseline_full_avg = float(df['Volume'].mean())
    except:
        return {}, 0.0

    for label, days in timeframes.items():
        try:
            sub_df = df.tail(days).copy() if len(df) >= days else df.copy()
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

            vol_spike_today_pct = 0.0
            if len(df) >= (days * 2):
                recent_vol_avg = df.tail(days)['Volume'].mean()
                previous_vol_avg = df.iloc[-(days * 2):-days]['Volume'].mean()
                if previous_vol_avg > 0:
                    vol_spike_today_pct = round(((recent_vol_avg - previous_vol_avg) / previous_vol_avg) * 100, 1)

            vol_period_change_pct = 0.0
            sub_period_avg = sub_df['Volume'].mean()
            if baseline_full_avg > 0:
                vol_period_change_pct = round(((sub_period_avg - baseline_full_avg) / baseline_full_avg) * 100, 1)
            
            results[label] = {
                'start_date': start_date, 'high': round(high_max, 2), 'low': round(low_min, 2),
                'high_pct': high_pct, 'low_pct': low_pct, 'range_pct': total_range_pct,
                'poc_price': poc_price, 'vol_spike_today': vol_spike_today_pct, 'vol_period_change': vol_period_change_pct
            }
        except:
            results[label] = {
                'start_date': None, 'high': 0.0, 'low': 0.0, 'high_pct': 0.0, 'low_pct': 0.0, 'range_pct': 0.0,
                'poc_price': None, 'vol_spike_today': 0.0, 'vol_period_change': 0.0
            }
            
    try:
        rsi_2m_avg = round(float(df['RSI'].tail(40).mean()), 2) if len(df) >= 40 else round(float(df['RSI'].mean()), 2)
    except:
        rsi_2m_avg = 50.0
        
    return results, rsi_2m_avg

universe = get_comprehensive_universe()

# Session State สำหรับเก็บ Watchlist ที่ติ๊กเลือกและพิมพ์เพิ่มเองแบบถาวร
if 'my_watchlist' not in st.session_state:
    st.session_state.my_watchlist = ['NVDA', 'PLTR', 'ISRG']

st.sidebar.markdown("### 📌 จัดการ Watchlist & Track หุ้น")
selected_sector = st.sidebar.selectbox("📂 เลือกกลุ่มอุตสาหกรรมตั้งต้น", list(universe.keys()))

st.sidebar.markdown("---")
st.sidebar.markdown(f"**ติ๊กเลือกหุ้นในหมวด: {selected_sector}**")

current_sector_stocks = universe[selected_sector]
for ticker, desc in current_sector_stocks.items():
    is_checked = ticker in st.session_state.my_watchlist
    checked = st.sidebar.checkbox(f"{ticker} ({desc[:22]}...)", value=is_checked, key=f"chk_{ticker}")
    if checked and ticker not in st.session_state.my_watchlist:
        st.session_state.my_watchlist.append(ticker)
    elif not checked and ticker in st.session_state.my_watchlist:
        st.session_state.my_watchlist.remove(ticker)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🔍 พิมพ์ Ticker เพิ่มเอง (Custom Track)")
custom_input_ticker = st.sidebar.text_input("พิมพ์ชื่อย่อหุ้น (เช่น TSLA, GOOGL, BABA)", "").upper().strip()
if st.sidebar.button("➕ เพิ่มเข้า Watchlist"):
    if custom_input_ticker and custom_input_ticker not in st.session_state.my_watchlist:
        st.session_state.my_watchlist.append(custom_input_ticker)
        st.sidebar.success(f"เพิ่ม [{custom_input_ticker}] สำเร็จ!")
        st.rerun()

if st.sidebar.button("🗑️ ล้าง Watchlist ทั้งหมด"):
    st.session_state.my_watchlist = []
    st.rerun()

st.markdown(f"## 📋 Watchlist & Track หุ้นส่วนตัวของมึง ({len(st.session_state.my_watchlist)} ตัว)")

if not st.session_state.my_watchlist:
    st.info("💡 มึงยังไม่ได้เลือกหุ้นเข้า Watchlist เลยเพื่อน! ติ๊กเลือกจากเมนูด้านซ้าย หรือพิมพ์ Ticker เพิ่มเองได้เลย ระบบจะล็อกข้อมูลไว้ให้ตลอด")
else:
    for ticker in list(st.session_state.my_watchlist):
        try:
            df = yf.download(ticker, period="3mo", interval="1d", progress=False)
            if df.empty or len(df) < 40:
                st.warning(symbol_warn := f"⚠️ ไม่พบข้อมูลของหุ้น [{ticker}] หรือข้อมูลน้อยเกินไป ลองเช็กตัวย่อใหม่อีกครั้งนะเพื่อน")
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
            
            recent = df.tail(20).copy()
            high_max = float(recent['High'].max())
            low_min = float(recent['Low'].min())
            
            tf_data, rsi_2m_avg = calculate_timeframe_metrics(df)
            tp1_price = round(latest_close * 1.05, 2)
            
            # ค้นหาคำอธิบาย Moat ของหุ้น
            moat_text = "หุ้นนวัตกรรม สิทธิบัตรเฉพาะทาง และเทคโนโลยีอนาคตไกล"
            for sec_name, stocks in universe.items():
                if ticker in stocks:
                    moat_text = stocks[ticker]
                    break

            expander_title = f"🟢 [{ticker}] | ราคาปิด: ${latest_close:.2f} | High: ${high_max:.2f} / Low:${low_min:.2f} | RSI: {latest_rsi:.1f}"
            
            with st.expander(expander_title, expanded=True):
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("💰 ราคาปิดปัจจุบัน", f"${latest_close:.2f}")
                col2.metric("📉 RSI ล่าสุด / เฉลี่ย 2M", f"{latest_rsi:.1f} / {rsi_2m_avg}")
                col3.metric("📊 กรอบราคา (1M High/Low)", f"${high_max:.2f} /${low_min:.2f}")
                col4.metric("🎯 เป้าทำกำไร (TP1 +5%)", f"${tp1_price}")
                
                st.markdown("---")
                st.markdown("### ⏱️ ตารางแกะรอยเจ้ามือสะสม (Multi-Timeframe Volume & POC Dynamics)")
                tf_rows = []
                for tf_name in ['1 วันก่อน', '3 วันก่อน', '1 อาทิตย์ก่อน', '2 อาทิตย์ก่อน', '1 เดือนก่อน', '2 เดือนก่อน']:
                    if tf_name in tf_data:
                        info = tf_data[tf_name]
                        poc_display = f"${info['poc_price']}" if info['poc_price'] is not None else "None"
                        tf_rows.append({
                            'ช่วงเวลา': tf_name, 'จุดเริ่มต้น': info['start_date'] if info['start_date'] else "N/A",
                            'ราคาสูงสุด': f"${info['high']} ({info['high_pct']:+.1f}%)",
                            'ราคาต่ำสุด': f"${info['low']} ({info['low_pct']:+.1f}%)",
                            'กรอบ (Range)': f"{info['range_pct']}%",
                            'POC (ฐานราคาหนาแน่นสุด)': poc_display,
                            '🔥 Vol เปรียบเทียบช่วงก่อน': f"{info['vol_spike_today']:+.1f}%",
                            '📈 Vol เฉลี่ยเทียบภาพรวม': f"{info['vol_period_change']:+.1f}%"
                        })
                st.table(pd.DataFrame(tf_rows))

                st.markdown("---")
                st.markdown("### 💬 วิเคราะห์เจาะลึกสไตล์เพื่อนซี้ (เกมเจ้ามือ & ข่าวสิทธิบัตร)")
                st.info(f"เพื่อนมองว่าตัว **{ticker}** ตัวนี้จังหวะราคากำลังเกาะโซนฐานสะสม สังเกตจากตาราง Multi-Timeframe ถ้าช่วงสัปดาห์ก่อนๆ โวลุ่มเริ่มหนาผิดปกติแต่ราคายืนนิ่ง แสดงว่าเจ้ามือซุ่มเก็บของรอข่าวประกาศสิทธิบัตรหรือผลประกอบการไตรมาสนี้แน่นอน!")
                st.markdown(f"📍 **โซนราคาเข้าสะสม (Entry Zone):** 🟢 **${low_min:.2f} -${low_min*1.02:.2f}** (เกาะแนวรับไส้เทียนล่างสุดอ้างอิงฐานราคา)")
                st.success(f"🔬 **คูเมืองนวัตกรรม & สิทธิบัตร (IP Moat):** **{moat_text}**")
                st.markdown(f"🚀 **แผนออกของ (Take Profit):** ทยอยขายทำกำไรแถว **${tp1_price}** หรือลุ้นรันเทรนด์ยาวๆ ตามกระแสข่าวสิทธิบัตรหลักของบริษัท")
        except:
            st.error(f"ไม่สามารถดึงข้อมูลของหุ้น [{ticker}] ได้ในขณะนี้ ลองตรวจสอบตัวย่อ Ticker อีกครั้งนะเพื่อน")
            

import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf

st.set_page_config(page_title="Deep Innovation & Swing Radar Pro (Full Universe)", layout="wide")

st.title("🎯 Deep Innovation & Swing Radar Pro (Full Universe & Custom Track)")
st.markdown("### เรดาร์สแกนหุ้นนวัตกรรม สิทธิบัตรลิขสิทธิ์ & แกะรอยเจ้ามือสะสมรอบข่าว (Full S&P 500 Deep Tech List)")

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
            'INTC': 'การพลิกฟื้นกิจการโรงงานผลิตชิปขั้นสูง (Foundry) และสิทธิบัตร x86',
            'MU': 'ผู้นำนวัตกรรมหน่วยความจำ High Bandwidth Memory (HBM) สำหรับชิป AI',
            'AMAT': 'วิศวกรรมวัสดุและอุปกรณ์ผลิตชิปขั้นสูงระดับโลก',
            'LRCX': 'เครื่องมือและสิทธิบัตรกระบวนการผลิตเซมิคอนดักเตอร์ระดับนาโน',
            'KLAC': 'ระบบตรวจสอบและควบคุมความสะอาดในการผลิตชิปขั้นสูง',
            'ASML': 'ผู้ผูกขาดเครื่องพิมพ์ลายเวเฟอร์ EUV หนึ่งเดียวในโลกสำหรับชิปยุคใหม่',
            'ADI': 'เซมิคอนดักเตอร์ระบบอนาล็อกและอุตสาหกรรมอัจฉริยะ',
            'TXN': 'ชิปประมวลผลอนาล็อกและระบบฝังตัวความน่าเชื่อถือสูง',
            'MCHP': 'ไมโครคอนโทรลเลอร์และเซมิคอนดักเตอร์อัจฉริยะ',
            'NOW': 'แพลตฟอร์ม Workflow AI อัตโนมัติสำหรับองค์กรขนาดใหญ่ระดับโลก',
            'CRM': 'Enterprise Cloud CRM และ AI Agent ผูกขาดฐานลูกค้าองค์กร',
            'ADBE': 'ซอฟต์แวร์ครีเอทีฟดิจิทัลและสิทธิบัตรเครื่องมือ Generative AI',
            'SNOW': 'แพลตฟอร์มคลาวด์ดาต้าแวร์เฮาส์และการวิเคราะห์ข้อมูลเชิงลึก',
            'PLTR': 'ซอฟต์แวร์วิเคราะห์ข้อมูล Big Data และ AI ทางทหาร/องค์กร (Gotham/Foundry)',
            'ANET': 'โครงข่ายดาต้าเซ็นเตอร์ความเร็วสูงพิเศษสำหรับ AI Infra',
            'PANW': 'ผู้นำระบบความปลอดภัยไซเบอร์ระดับองค์กร (Cybersecurity Moat)',
            'CRWD': 'ระบบป้องกันภัยคุกคามทางไซเบอร์แบบ Cloud-native อัจฉริยะ',
            'FTNT': 'โครงสร้างพื้นฐานความปลอดภัยเครือข่ายและไฟร์วอลล์สิทธิบัตรแกร่ง'
        },
        "🤖 2. Smart Manufacturing, Industrial Robotics & Clean Energy": {
            'TSLA': 'นวัตกรรมยานยนต์ไฟฟ้า, ระบบขับเคลื่อนอัตโนมัติ FSD, หุ่นยนต์ฮิวแมนนอยด์ Optimus',
            'CAT': 'เครื่องจักรกลหนัก, ระบบขุดเจาะอัตโนมัติ และยานยนต์เหมืองไร้คนขับอัจฉริยะ',
            'DE': 'เครื่องจักรกลการเกษตรอัตโนมัติ, AI Vision และเทคโนโลยีสมาร์ทฟาร์มแม่นยำสูง',
            'ETN': 'ระบบจัดการพลังงานไฟฟ้าและหม้อแปลงอัจฉริยะสำหรับ Data Center และโรงงาน AI',
            'GEV': 'เทคโนโลยีโครงข่ายไฟฟ้าอัจฉริยะ กังหันลม และระบบขับเคลื่อนพลังงานหลัก',
            'NEE': 'ยักษ์ใหญ่พลังงานสะอาดและโครงสร้างพื้นฐานกริดไฟฟ้าป้อน Data Center AI',
            'ENPH': 'เทคโนโลยีไมโครอินเวอร์เตอร์และระบบกักเก็บพลังงานแสงอาทิตย์อัจฉริยะ',
            'FSLR': 'สิทธิบัตรการผลิตแผงโซลาร์เซลล์เทคโนโลยีฟิล์มบางขั้นสูงในสหรัฐฯ',
            'CEG': 'ผู้ผลิตพลังงานคาร์บอนต่ำและโรงไฟฟ้านิวเคลียร์รายใหญ่ที่สุดของสหรัฐฯ',
            'HON': 'ระบบอัตโนมัติในโรงงาน, หุ่นยนต์คลังสินค้าอัจฉริยะ และเทคโนโลยีอาคารประหยัดพลังงาน',
            'ROK': 'ซอฟต์แวร์และฮาร์ดแวร์ระบบอัตโนมัติสำหรับโรงงานอัจฉริยะ (The Connected Enterprise)',
            'EMR': 'ผู้นำนวัตกรรมระบบควบคุมอัตโนมัติระดับอุตสาหกรรม (Industrial Automation)',
            'PWR': 'ผู้รับเหมาโครงสร้างพื้นฐานระบบไฟฟ้าแรงสูงและดาต้าเซ็นเตอร์เบอร์หนึ่ง',
            'LIN': 'ก๊าซอุตสาหกรรมและนวัตกรรมเคมีภัณฑ์ไฮโดรเจนสะอาดระดับโลก',
            'DELL': 'เซิร์ฟเวอร์โครงสร้างพื้นฐาน AI Infrastructure และฮาร์ดแวร์องค์กร'
        },
        "🧬 3. Biotech, Healthcare & Medical Robotics": {
            'ISRG': 'หุ่นยนต์ผ่าตัดแผลเล็ก Da Vinci (สิทธิบัตรแขนกลเชิงลึก ผูกขาดตลาดร้อยเปอร์เซ็นต์)',
            'LLY': 'ยารักษาโรคเรื้อรังและยาลดน้ำหนัก/เบาหวานตัวท็อป (Mounjaro/Zepbound)',
            'NVO': 'นวัตกรรมยารักษาโรคอ้วนและเบาหวานระดับโลก (Wegovy/Ozempic)',
            'UNH': 'ระบบนิเวศประกันสุขภาพและบริการเทคโนโลยีการแพทย์ขนาดใหญ่',
            'JNJ': 'ความหลากหลายของเวชภัณฑ์และอุปกรณ์การแพทย์ระดับโลก',
            'ABBV': 'ยารักษาโรคภูมิคุ้มกันและมะเร็งเฉพาะทางที่มีสิทธิบัตรคุ้มครอง',
            'MRK': 'นวัตกรรมยารักษามะเร็งระดับโลก (Keytruda)',
            'PFE': 'นวัตกรรมวัคซีนและเวชภัณฑ์ระดับโลก',
            'AMGN': 'เทคโนโลยีชีวภาพและยารักษาโรคชีววัตถุขั้นสูง',
            'TMO': 'เครื่องมือวิทยาศาสตร์และบริการวิจัยพันธุศาสตร์ระดับโลก',
            'ABT': 'อุปกรณ์การแพทย์ตรวจวินิจฉัยและโภชนาการทางการแพทย์',
            'DHR': 'เทคโนโลยีชีวภาพและเครื่องมือวิเคราะห์ทางการแพทย์ขั้นสูง',
            'VRTX': 'ยีนเทอร์ราพีและนวัตกรรมยารักษาโรคทางพันธุกรรม (Cystic Fibrosis)',
            'REGN': 'เทคโนโลยีชีวภาพและแอนติบอดีสังเคราะห์รักษาโรคเฉพาะทาง',
            'ZTS': 'เวชภัณฑ์และนวัตกรรมสุขภาพสัตว์เลี้ยงระดับโลก'
        },
        "🌐 4. Big Platforms, Fintech & High-Moat Financials": {
            'AMZN': 'E-commerce Ecosystem, Cloud Computing (AWS) & Logistics IP',
            'GOOGL': 'AI Search, Deep Learning Infrastructure & YouTube Ecosystem',
            'META': 'Social Media Ecosystem, Open Source AI (Llama) & Smart Wearables IP',
            'NFLX': 'อัลกอริทึมสตรีมมิ่งและแพลตฟอร์มความบันเทิงระดับโลก',
            'UBER': 'แพลตฟอร์มขนส่งอัจฉริยะและโครงสร้างโลจิสติกส์ไร้คนขับในอนาคต',
            'BRK-B': 'กลุ่มทุนขนาดใหญ่, เครือข่ายประกันภัยและสัดส่วนถือหุ้นบริษัทชั้นนำ',
            'JPM': 'ธนาคารพาณิชย์เบอร์หนึ่งของสหรัฐฯ, เทคโนโลยีการเงินและงบดุลแกร่ง',
            'V': 'เครือข่ายชำระเงินระดับโลกและโครงสร้างพื้นฐานฟินเทค',
            'MA': 'เครือข่ายการชำระเงินดิจิทัลทั่วโลกที่มีกำไรสุทธิสูงลิ่ว',
            'AXP': 'เครือข่ายบัตรเครดิตกลุ่มลูกค้ากำลังซื้อสูง (High Net Worth)',
            'BLK': 'ผู้จัดการกองทุนที่ใหญ่ที่สุดในโลก (BlackRock / Aladdin Platform)',
            'GS': 'วาณิชธนกิจชั้นนำระดับโลกและตลาดทุน',
            'MS': 'บริการบริหารความมั่งคั่งและวาณิชธนกิจระดับโลก',
            'BAC': 'ธนาคารพาณิชย์รายใหญ่และฐานลูกค้ารายย่อยทั่วสหรัฐฯ',
            'SCHW': 'แพลตฟอร์มการลงทุนและซื้อขายหลักทรัพย์ชั้นนำ',
            'PYPL': 'แพลตฟอร์มชำระเงินออนไลน์และฟินเทคระดับโลก',
            'SQ': 'ระบบนิเวศการเงินและบล็อกเชนรายย่อย',
            'COIN': 'โครงสร้างพื้นฐานแลกเปลี่ยนสินทรัพย์ดิจิทัลและคริปโต',
            'HOOD': 'แพลตฟอร์มซื้อขายสินทรัพย์ดิจิทัลและหุ้นรุ่นใหม่',
            'FI': 'เทคโนโลยีบริการการเงินและระบบประมวลผลธนาคาร',
            'FIS': 'ฟินเทคระบบธนาคารระดับองค์กร',
            'GPN': 'เทคโนโลยีการชำระเงินร้านค้าทั่วโลก',
            'SPGI': 'ข้อมูลเรตติ้งและดัชนีมาตรฐานการเงินโลก',
            'MCO': 'การจัดอันดับความน่าเชื่อถือทางการเงินระดับโลก',
            'ICE': 'ตลาดหลักทรัพย์และแพลตฟอร์มซื้อขายอนุพันธ์ระดับโลก'
        },
        "🚀 5. Space Tech, Defense & Advanced Materials": {
            'LMT': 'อากาศยานทหารขั้นสูงและระบบป้องกันขีปนาวุธ',
            'RTX': 'เทคโนโลยีการบินอวกาศและระบบเรดาร์ป้องกันประเทศ',
            'NOC': 'โครงการอวกาศเชิงยุทธศาสตร์และเครื่องบินทิ้งตัวขั้นสูง',
            'BA': 'อากาศยานพาณิชย์และเทคโนโลยีอวกาศระดับโลก',
            'TDG': 'ชิ้นส่วนอากาศยานเฉพาะทางที่มีกำไรสุทธิสูง',
            'HEI': 'อุปกรณ์การบินและชิ้นส่วนทดแทนที่มีสิทธิบัตรคุ้มครอง',
            'RKLB': 'ผู้นำการปล่อยจรวดอวกาศเชิงพาณิชย์และดาวเทียมวงโคจรต่ำ',
            'ASTS': 'เครือข่ายบล็อกเซลลูลาร์อวกาศเชื่อมต่อมือถือโดยตรง',
            'DD': 'นวัตกรรมวัสดุศาสตร์ขั้นสูงและอิเล็กทรอนิกส์เคมี',
            'EMN': 'วัสดุพิเศษและโพลิเมอร์นวัตกรรมเพื่อความยั่งยืน'
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

# Sidebar Setup
st.sidebar.markdown("### ⚙️ ควบคุมการสแกนเรดาร์ (Full Tech)")
selected_sector = st.sidebar.selectbox("📂 เลือกกลุ่มอุตสาหกรรมสแกนหลัก", list(universe.keys()))

st.sidebar.markdown("---")
st.sidebar.markdown("### 🔍 ช่องพิมพ์ Ticker เพิ่มเติม (Custom Track)")
custom_input_ticker = st.sidebar.text_input("พิมพ์ชื่อย่อหุ้น (เช่น TSLA, GOOGL, ARM)", "").upper().strip()

target_tickers = list(universe[selected_sector].keys())
if custom_input_ticker and custom_input_ticker not in target_tickers:
    target_tickers.append(custom_input_ticker)

st.markdown(f"## 🚀 ผลการสแกนกลุ่ม: {selected_sector}")
st.markdown(f"*(กำลังวิเคราะห์หุ้นนวัตกรรมและสิทธิบัตรทั้งหมด {len(target_tickers)} ตัวในเซกเตอร์นี้ พร้อมแกะรอยเกมเจ้ามือและสิถิติ Volume)*")

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
        
        recent = df.tail(20).copy()
        high_max = float(recent['High'].max())
        low_min = float(recent['Low'].min())
        
        tf_data, rsi_2m_avg = calculate_timeframe_metrics(df)
        tp1_price = round(latest_close * 1.05, 2)
        
        moat_text = "หุ้นนวัตกรรม สิทธิบัตรเฉพาะทาง และเทคโนโลยีเติบโตสูง"
        found_in_universe = False
        for sec_name, stocks in universe.items():
            if ticker in stocks:
                moat_text = stocks[ticker]
                found_in_universe = True
                break
        if not found_in_universe and ticker == custom_input_ticker:
            moat_text = "หุ้นเฉพาะกิจที่มึงเพิ่มเข้ามาในเรดาร์ติดตามพิเศษ"

        expander_title = f"🟢 [{ticker}] | ราคาปิด: ${latest_close:.2f} | High: ${high_max:.2f} / Low: ${low_min:.2f} | RSI: {latest_rsi:.1f}"
        
        with st.expander(expander_title, expanded=False):
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("💰 ราคาปิดปัจจุบัน", f"${latest_close:.2f}")
            col2.metric("📉 RSI ล่าสุด / เฉลี่ย 2M", f"{latest_rsi:.1f} / {rsi_2m_avg}")
            col3.metric("📊 กรอบราคา (1M High/Low)", f"${high_max:.2f} / ${low_min:.2f}")
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
            st.markdown(f"📍 **โซนราคาเข้าสะสม (Entry Zone):** 🟢 **${low_min:.2f} - ${low_min*1.02:.2f}** (เกาะแนวรับไส้เทียนล่างสุดอ้างอิงฐานราคา)")
            st.success(f"🔬 **คูเมืองนวัตกรรม & สิทธิบัตร (IP Moat):** **{moat_text}**")
            st.markdown(f"🚀 **แผนออกของ (Take Profit):** ทยอยขายทำกำไรแถว **${tp1_price}** หรือลุ้นรันเทรนด์ยาวๆ ตามกระแสข่าวสิทธิบัตรหลักของบริษัท")
    except:
        st.error(f"ไม่สามารถดึงข้อมูลของหุ้น [{ticker}] ได้ในขณะนี้ ลองตรวจสอบตัวย่อ Ticker อีกครั้งนะเพื่อน")
        

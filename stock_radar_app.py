import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf

st.set_page_config(page_title="Deep Innovation & Swing Trading Radar Pro", layout="wide")

st.title("🎯 Deep Innovation & Swing Trading Radar Pro (AI Analyst Friend Edition)")
st.markdown("### เรดาร์สแกนหุ้นนวัตกรรม, สิทธิบัตรระดับโลก, AI Infrastructure พร้อมเพื่อนซี้ช่วยวิเคราะห์สถานะและดักจับเกมเจ้ามือ")

@st.cache_data(ttl=86400)
def get_comprehensive_universe():
    universe = {
        "💻 Information Technology (เทคโนโลยี, ชิป AI & ซอฟต์แวร์ระบบ)": {
            'AAPL': 'Ecosystem ฮาร์ดแวร์และบริการ, สิทธิบัตรชิป Apple Silicon',
            'MSFT': 'Moat ซอฟต์แวร์องค์กร, คลาวด์ Azure, ผูกขาด AI ร่วมกับ OpenAI',
            'NVDA': 'สถาปัตยกรรมชิป AI & CUDA Software Ecosystem ผูกขาดตลาด',
            'AVGO': 'ชิปเครือข่ายความเร็วสูงพิเศษ & Custom AI Silicon สำหรับดาต้าเซ็นเตอร์',
            'ARM': 'เจ้าของสถาปัตยกรรมชิปมือถือและชิป AI ใช้พลังงานต่ำทั่วโลก',
            'CRM': 'Enterprise Cloud CRM และ AI Agent ผูกขาดฐานลูกค้าองค์กร',
            'ADBE': 'ซอฟต์แวร์ครีเอทีฟดิจิทัลและสิทธิบัตรเครื่องมือ Generative AI',
            'ACN': 'บริการที่ปรึกษาเทคโนโลยีและดิจิทัลทรานส์ฟอร์เมชันระดับโลก',
            'CSCO': 'โครงสร้างพื้นฐานเครือข่ายอินเทอร์เน็ตและสิทธิบัตรความปลอดภัย',
            'QCOM': 'สิทธิบัตรหลักเทคโนโลยีสื่อสารไร้สาย 5G/6G และ Edge AI ชิป'
        },
        "🧬 Health Care & Bio-Tech (การแพทย์, ไบโอเทค & หุ่นยนต์ผ่าตัด)": {
            'LLY': 'ยารักษาโรคเรื้อรังและยาลดน้ำหนัก/เบาหวาน (Mounjaro/Zepbound)',
            'UNH': 'ระบบนิเวศประกันสุขภาพและบริการเทคโนโลยีการแพทย์ขนาดใหญ่',
            'JNJ': 'ความหลากหลายของเวชภัณฑ์และอุปกรณ์การแพทย์ระดับโลก',
            'ABBV': 'ยารักษาโรคภูมิคุ้มกันและมะเร็งเฉพาะทางที่มีสิทธิบัตรคุ้มครอง',
            'MRK': 'นวัตกรรมยารักษามะเร็งระดับโลก (Keytruda)',
            'TMO': 'เครื่องมือวิทยาศาสตร์และบริการวิจัยพันธุศาสตร์ระดับโลก',
            'ISRG': 'หุ่นยนต์ผ่าตัดแผลเล็ก Da Vinci (สิทธิบัตรแขนกลเชิงลึก ผูกขาดตลาดร้อยเปอร์เซ็นต์)',
            'ABT': 'อุปกรณ์การแพทย์ตรวจวินิจฉัยและโภชนาการทางการแพทย์',
            'PFE': 'นวัตกรรมวัคซีนและเวชภัณฑ์ระดับโลก',
            'AMGN': 'เทคโนโลยีชีวภาพและยารักษาโรคชีววัตถุขั้นสูง'
        },
        "⚡ Power, Robotics & Clean Energy (พลังงาน AI, โครงข่ายอัจฉริยะ & หุ่นยนต์)": {
            'NEE': 'ยักษ์ใหญ่พลังงานสะอาดและโครงสร้างพื้นฐานกริดไฟฟ้าป้อน Data Center AI',
            'GEV': 'เทคโนโลยีโครงข่ายไฟฟ้าอัจฉริยะ กังหันลม และระบบขับเคลื่อนพลังงานหลัก',
            'ETN': 'ระบบจัดการพลังงานไฟฟ้าและหม้อแปลงอัจฉริยะสำหรับ Data Center และโรงงาน AI',
            'PWR': 'ผู้รับเหมาโครงสร้างพื้นฐานระบบไฟฟ้าแรงสูงและดาต้าเซ็นเตอร์เบอร์หนึ่ง',
            'CAT': 'เครื่องจักรกลหนัก ระบบขุดเจาะอัตโนมัติ และยานยนต์เหมืองไร้คนขับ',
            'DE': 'เครื่องจักรกลการเกษตรอัจฉริยะ, AI Vision และเทคโนโลยีฟาร์มแม่นยำ',
            'HON': 'ระบบอัตโนมัติในโรงงาน หุ่นยนต์คลังสินค้า และเทคโนโลยีอาคารอัจฉริยะ',
            'UBER': 'แพลตฟอร์มขนส่งอัจฉริยะและโครงสร้างโลจิสติกส์ไร้คนขับในอนาคต',
            'RTX': 'เทคโนโลยีการบินอวกาศ เซ็นเซอร์อัจฉริยะ และระบบป้องกันประเทศ',
            'LMT': 'เทคโนโลยีการบินทหาร ระบบอัตโนมัติ และระบบป้องกันประเทศขั้นสูง'
        },
        "💡 Utilities & Essential Infrastructure (สาธารณูปโภค S&P 500 & โครงสร้างพื้นฐานมั่นคง)": {
            'NEE': 'ผู้นำโรงไฟฟ้าพลังงานทดแทนและสาธารณูปโภคไฟฟ้าขนาดใหญ่ที่สุดในสหรัฐฯ',
            'DUK': 'บริษัทสาธารณูปโภคไฟฟ้าและก๊าซธรรมชาติฐานลูกค้าหลายล้านครัวเรือน กระแสเงินสดมั่นคง',
            'SO': 'ยักษ์ใหญ่ด้านพลังงานและโครงข่ายไฟฟ้าพลังงานนิวเคลียร์และฟอสซิลสะอาด',
            'CEG': 'ผู้ผลิตพลังงานคาร์บอนด์ต่ำและโรงไฟฟ้านิวเคลียร์รายใหญ่ที่สุดของสหรัฐฯ (พลังงานป้อน AI)',
            'AEP': 'เครือข่ายส่งไฟฟ้าแรงสูงและสาธารณูปโภคไฟฟ้าครอบคลุมหลายรัฐ',
            'SRE': 'โครงสร้างพื้นฐานก๊าซธรรมชาติและระบบส่งไฟฟ้ากำลังซื้อสูง',
            'PCG': 'สาธารณูปโภคไฟฟ้าแคลิฟอร์เนีย โครงข่ายพลังงานสะอาดและฟื้นฟูกริดอัจฉริยะ',
            'EXC': 'บริษัทโฮลดิ้งสาธารณูปโภคไฟฟ้าและระบบส่งจ่ายพลังงานรายใหญ่',
            'XEL': 'ผู้นำด้านพลังงานลมและระบบส่งไฟฟ้าอัจฉริยะที่เป็นมิตรต่อสิ่งแวดล้อม',
            'ED': 'สาธารณูปโภคไฟฟ้าและก๊าซเขตมหานครนิวยอร์ก ปันผลมั่นคงระดับตำนาน'
        },
        "💰 Financials & High-Moat Assets (การเงิน, ธนาคาร & โครงสร้างแกร่ง)": {
            'BRK-B': 'กลุ่มทุนขนาดใหญ่, เครือข่ายประกันภัยและสัดส่วนถือหุ้นบริษัทชั้นนำ',
            'JPM': 'ธนาคารพาณิชย์เบอร์หนึ่งของสหรัฐฯ, เทคโนโลยีการเงินและงบดุลแกร่ง',
            'V': 'เครือข่ายชำระเงินระดับโลกและโครงสร้างพื้นฐานฟินเทค',
            'MA': 'เครือข่ายการชำระเงินดิจิทัลทั่วโลกที่มีกำไรสุทธิสูงลิ่ว',
            'BAC': 'ธนาคารพาณิชย์รายใหญ่และฐานลูกค้ารายย่อยทั่วสหรัฐฯ',
            'GS': 'วาณิชธนกิจชั้นนำระดับโลกและตลาดทุน',
            'AXP': 'เครือข่ายบัตรเครดิตกลุ่มลูกค้ากำลังซื้อสูง (High Net Worth)',
            'BLK': 'ผู้จัดการกองทุนที่ใหญ่ที่สุดในโลก (BlackRock / Aladdin Platform)',
            'SPGI': 'ผู้ให้บริการจัดอันดับความน่าเชื่อถือและข้อมูลการเงินโลก',
            'ICE': 'เจ้าของตลาดหลักทรัพย์และแพลตฟอร์มซื้อขายอนุพันธ์/พลังงาน'
        },
        "🌐 Big Platforms & Digital Ecosystem (แพลตฟอร์มโซเชียล & คลาวด์ยักษ์ใหญ่)": {
            'AMZN': 'E-commerce Ecosystem, Cloud Computing (AWS) & Logistics IP',
            'TSLA': 'นวัตกรรมยานยนต์ไฟฟ้า, ระบบขับเคลื่อนอัตโนมัติ FSD, หุ่นยนต์ Optimus และพลังงาน',
            'GOOGL': 'AI Search, Deep Learning Infrastructure & YouTube Ecosystem',
            'META': 'Social Media Ecosystem, Open Source AI (Llama) & Smart Wearables IP',
            'NFLX': 'อัลกอริทึมสตรีมมิ่งและแพลตฟอร์มความบันเทิงระดับโลก',
            'DIS': 'ลิขสิทธิ์แฟรนไชส์สื่อบันเทิงและสตรีมมิ่งระดับโลก',
            'NOW': 'แพลตฟอร์ม Workflow Software อัตโนมัติสำหรับองค์กรขนาดใหญ่ระดับโลก'
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

        avg_sub_vol = sub_df['Volume'].mean()
        baseline_start_idx = max(0, len(df) - (days * 2))
        baseline_end_idx = max(0, len(df) - days)
        
        if baseline_end_idx > baseline_start_idx:
            baseline_vol = df['Volume'].iloc[baseline_start_idx:baseline_end_idx].mean()
        else:
            baseline_vol = df['Volume'].mean()
            
        vol_change_pct = round(((avg_sub_vol - baseline_vol) / baseline_vol) * 100, 1) if baseline_vol > 0 else 0.0
        
        results[label] = {
            'start_date': start_date, 'high': round(high_max, 2), 'low': round(low_min, 2),
            'high_pct': high_pct, 'low_pct': low_pct, 'range_pct': total_range_pct,
            'poc_price': poc_price, 'vol_change_pct': vol_change_pct
        }
        
    rsi_2m_avg = round(float(df['RSI'].tail(40).mean()), 2) if len(df) >= 40 else round(float(df['RSI'].mean()), 2)
    return results, rsi_2m_avg

def calculate_rsi(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    return 100 - (100 / (1 + (gain / loss)))

def friend_expert_analysis(ticker, moat_story, latest_rsi, range_pct, vol_change, rsi_2m_avg, tf_data):
    """ระบบวิเคราะห์สไตล์เพื่อนซี้กูรูหุ้นสิทธิบัตรและเซียนเล่นรอบ ตีกรอบสถานะให้ชัดเจน"""
    
    # เช็คสัญญาณ Volume Divergence (หลอกลวง / แจกของ)
    vol_3d_change = tf_data.get('3 วัน', {}).get('vol_change_pct', 0)
    
    analysis_blocks = []
    
    # 1. วิเคราะห์สถานะทางเทคนิคและพฤติกรรมเจ้ามือ
    if range_pct <= 7.0 and 40 <= latest_rsi <= 58 and vol_change < 10:
        status_tag = "🟡 **[สถานะ: กำลังสะสมพลังในกรอบแคบ / Smart Money Accumulation]**"
        commentary = (
            f"เพื่อนว่าตัว **{ticker}** ตัวนี้ทรงสวยวะ กราฟซึมตัวออกข้าง ไร้แรงขายทุบหนัก "
            f"วอลุ่มเบาบางแห้งสนิทแบบนี้ ส่อเค้าว่ารายใหญ่กำลังอมของเก็บเงียบๆ รอข่าวสิทธิบัตรหรือผลประกอบการออก "
            f"เหมาะสำหรับทยอยสะสม (Accumulate) แถวโซนแนวรับ ไม่ต้องรีบไล่ราคา ปลอดภัยสูงมาก"
        )
    elif latest_rsi > rsi_2m_avg and 45 <= latest_rsi <= 68 and vol_change >= 5:
        status_tag = "🟢 **[สถานะ: เริ่มส่งสัญญาณ Turnaround / กลิ่นอายขาขึ้นรอบใหม่]**"
        commentary = (
            f"เฮ้ย ตัว **{ticker}** น่าสนใจ โมเมนตัมกำลังยกตัวตัดค่าเฉลี่ยขึ้นมา RSI ไต่ระดับออกจากโซนล่าง "
            f"ประกอบกับมีวอลุ่มเริ่มหนุนหนานขึ้น แปลว่าเม็ดเงินลงทุนเริ่มไหลกลับมาเก็งกำไรในสตอรี่นวัตกรรมและเทคโนโลยีตัวนี้แล้ว "
            f"เข้าเกณฑ์หุ้นกำลัง Turnaround เตรียมตัววิ่งตามรอบใหญ่ได้"
        )
    elif range_pct > 7.0 and vol_change >= 15:
        if vol_3d_change < -20:
            status_tag = "🔴 **[สถานะอันตราย: ระวังโดนแจกของ / Bull Trap (Volume Divergence)]**"
            commentary = (
                f"มึงระวังให้ดีนะเว้ย ตัว **{ticker}** ราคาทำท่าจะวิ่งหรือยืนสูง แต่พอมาเช็กวอลุ่ม 3 วันล่าสุด "
                f"ปรากฏว่า **% Vol Change ดันติดลบหนักสวนทางกับราคา** แบบนี้แปลว่าเจ้ามืออาจกำลังรินของแจกเม่า "
                f"ระวังโดนลากไปเชือด อย่าเพิ่งเอาเงินไปเสี่ยงไล่ราคาเด็ดขาด!"
            )
        else:
            status_tag = "🔥 **[สถานะ: กำลังเหวี่ยงกรอบแรง / โมเมนตัมเบรกเอาท์เด่นชัด (Volatile Breakout)]**"
            commentary = (
                f"ตัว **{ticker}** กำลังซิ่งตามกระแสข่าวร้อนแรง ราคาสวิงตัวกว้างและวอลุ่มหนาแน่นสุดๆ "
                f"เหมาะกับสาย Swing Trading เล่นรอบสั้นเกาะกระแสเทรนด์นวัตกรรม แต่ต้องรัดกุม ตั้งจุด Trailing Stop ไว้ด้วย อย่าประมาท!"
            )
    else:
        status_tag = "⚪ **[สถานะ: พักตัวตามรอบปกติ / รอสะสมพลัง (Consolidation)]**"
        commentary = (
            f"หุ้น **{ticker}** ตัวนี้ยังแกว่งตัวตามกรอบเทคนิคปกติ ไม่มีอะไรหวือหวา "
            f"ให้โฟกัสที่สตอรี่สิทธิบัตรและนวัตกรรมหลักของบริษัทนี้ไปก่อน รอจังหวะราคาลงมาแตะแนวรับค่อยหาจังหวะเก็บเพิ่ม"
        )

    # 2. วิเคราะห์เชิงลึกด้านสิทธิบัตรและนวัตกรรม (IP Moat Value)
    ip_analysis = (
        f"🔬 **มุมมองสิทธิบัตรและคูเมืองธุรกิจ (IP Moat & Patent Value):** "
        f"จุดเด่นของ {ticker} คือ *'{moat_story}'* ซึ่งในโลกอนาคตบริษัทที่มีสิทธิบัตรคุ้มครองและเทคโนโลยีเฉพาะตัวแบบนี้ "
        f"จะมีอำนาจต่อรองสูงมาก คู่แข่งเจาะเข้ามาแย่งส่วนแบ่งตลาดยาก กระแสเงินสดในระยะยาวจะมั่นคง "
        f"เหมาะกับการถือลงทุนกินรอบใหญ่ตามรอบวัฏจักรนวัตกรรมโลก"
    )

    return status_tag, commentary, ip_analysis

universe = get_comprehensive_universe()

# --- SIDEBAR CONFIGURATION ---
st.sidebar.markdown("### ⚙️ ตั้งค่าการสแกนหุ้นเล่นรอบ")
selected_sector = st.sidebar.selectbox("📂 เลือกกลุ่มอุตสาหกรรม (Sector)", list(universe.keys()))
strategy_mode = st.sidebar.selectbox("⚙️ เลือกโหมดกลยุทธ์การเล่นรอบ", [
    "1. โหมดสะสมกรอบแคบ (RSI 40-60 และกรอบราคา 1 เดือนไม่เกิน 10% - ปลอดภัยสูง/รอข่าวเบรก)", 
    "2. โหมดโมเมนตัมเบรกเอาท์ตามกระแส (วอลุ่มพุ่งและราคาสวิงตัวเด่นชัด - เกาะเทรนด์ร้อน)"
])

st.markdown(f"## 🎯 สแกนหาหุ้นเล่นรอบตามเทรนด์ใน Sector: **{selected_sector}**")

if st.button("🚀 เริ่มคัดกรองหุ้นตามเกณฑ์เล่นรอบ"):
    target_tickers = universe[selected_sector]
    matched_data = []
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    total_tickers = len(target_tickers)
    
    for i, (ticker, moat_story) in enumerate(target_tickers.items()):
        status_text.text(f"กำลังวิเคราะห์หุ้น [{ticker}] ({i+1}/{total_tickers})...")
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
            
            vol_change_val = round(((last_vol - last_vol_ma) / last_vol_ma) * 100, 1) if last_vol_ma > 0 else 0.0
            
            is_matched = False
            if "โหมดสะสมกรอบแคบ" in strategy_mode:
                if range_pct <= 0.10 and 40 <= latest_rsi <= 60 and last_vol <= (last_vol_ma * 1.1):
                    is_matched = True
            else:
                vol_spike = last_vol >= (last_vol_ma * 1.3)
                if range_pct >= 0.05 and latest_rsi >= 45 and vol_spike:
                    is_matched = True

            if is_matched:
                tf_data, rsi_2m_avg = calculate_timeframe_metrics(df)
                tp1_price = round(latest_close * 1.05, 2)
                
                # เรียกใช้งานสมองกลเพื่อนซี้วิเคราะห์สถานะ
                status_tag, commentary, ip_analysis = friend_expert_analysis(
                    ticker, moat_story, latest_rsi, range_pct * 100, vol_change_val, rsi_2m_avg, tf_data
                )
                
                matched_data.append({
                    'Ticker': ticker, 'Moat': moat_story,
                    'Close': round(latest_close, 2), 'Range_Pct': round(range_pct * 100, 1),
                    'RSI_Latest': round(latest_rsi, 2), 'RSI_2M_Avg': rsi_2m_avg,
                    'TF_Data': tf_data, 'TP1': tp1_price,
                    'Low_Min': round(low_min, 2),
                    'Status_Tag': status_tag, 'Commentary': commentary, 'IP_Analysis': ip_analysis
                })
        except:
            continue

    status_text.empty()
    progress_bar.empty()

    if matched_data:
        st.success(f"🎯 คัดกรองหุ้นที่ผ่านเกณฑ์เล่นรอบสำเร็จ พบทั้งหมด **{len(matched_data)} ตัว**!")
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
                st.markdown(f"🔬 **จุดแข็งสิทธิบัตร & IP Moat:** **{item['Moat']}**")
                st.markdown(f"📍 **จุดเข้าซื้อเชิงกลยุทธ์ (Entry Zone):** 🟢 **${item['Low_Min']} - ${round(item['Low_Min']*1.02, 2)}** (โซนเก็บของไส้เทียนล่าง)")

                # --- ส่วนบทวิเคราะห์จากเพื่อนซี้กูรูหุ้นสิทธิบัตร ---
                st.markdown("---")
                st.markdown("### 💬 มุมมองเพื่อนซี้ (วิเคราะห์สถานะ & เตือนภัยเกมเจ้ามือ)")
                st.markdown(item['Status_Tag'])
                st.info(item['Commentary'])
                st.success(item['IP_Analysis'])

                st.markdown("---")
                st.markdown("### ⏱️ เปรียบเทียบกรอบราคา, ราคาหนาแน่นสุด (POC) และ % Volume Change")
                tf_rows = []
                for tf_name in ['เมื่อวันก่อน', '3 วัน', '1 อาทิตย์', '2 อาทิตย์', '1 เดือน', '2 เดือน']:
                    if tf_name in item['TF_Data']:
                        info = item['TF_Data'][tf_name]
                        tf_rows.append({
                            'ช่วงเวลา': tf_name, 'วันที่อ้างอิง': info['start_date'],
                            'ราคาสูงสุด (High)': f"${info['high']} ({info['high_pct']:+.1f}%)",
                            'ราคาต่ำสุด (Low)': f"${info['low']} ({info['low_pct']:+.1f}%)",
                            'ความกว้างกรอบ': f"{info['range_pct']}%",
                            'POC (ราคาหนาแน่นสุด)': f"${info['poc_price']}",
                            '% Vol Change': f"{info['vol_change_pct']:+.1f}%"
                        })
                st.table(pd.DataFrame(tf_rows))
        st.markdown("---")
    else:
        st.warning("ไม่มีหุ้นตัวไหนใน Sector นี้ผ่านเกณฑ์ในรอบนี้ ลองสลับโหมดกลยุทธ์หรือเปลี่ยน Sector ดูก่อนเพื่อน!")

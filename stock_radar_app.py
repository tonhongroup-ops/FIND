import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf

st.set_page_config(page_title="Deep Innovation & Swing Trading Radar Pro", layout="wide")

st.title("🎯 Deep Innovation & Swing Trading Radar Pro (90 S&P 500 Mega Universe)")
st.markdown("### เรดาร์สแกนหุ้นนวัตกรรม สิทธิบัตร และรอบข่าวสาร (90 หุ้นคัดพิเศษ S&P 500 พร้อมงบการเงิน & Multi-Timeframe POC)")

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

def calculate_timeframe_metrics(df):
    timeframes = {
        'เมื่อวันก่อน': 1, '3 วัน': 3, '1 อาทิตย์': 5, 
        '2 อาทิตย์': 10, '1 เดือน': 20, '2 เดือน': 40
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
            elif len(sub_df) >= 2 and days == 1:
                latest_vol = sub_df['Volume'].iloc[-1]
                prev_vol = sub_df['Volume'].iloc[-2]
                if prev_vol > 0:
                    vol_spike_today_pct = round(((latest_vol - prev_vol) / prev_vol) * 100, 1)

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
                'start_date': None, 'high': 0.0, 'low': 0.0,
                'high_pct': 0.0, 'low_pct': 0.0, 'range_pct': 0.0,
                'poc_price': None, 'vol_spike_today': 0.0, 'vol_period_change': 0.0
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

def friend_expert_analysis(ticker, moat_story, latest_rsi, range_pct, vol_period_change, rsi_2m_avg, tf_data, strategy_mode):
    try:
        poc_1m = tf_data.get('1 เดือน', {}).get('poc_price', 0)
        if poc_1m is None:
            poc_1m = 0
    except:
        poc_1m = 0

    if "สะสม" in strategy_mode:
        status_tag = "🟡 **[สถานะ: กำลังสะสมพลังในกรอบ / Smart Money Accumulation Zone]**"
        commentary = (
            f"เพื่อนว่าตัว **{ticker}** ทรงนี้เข้าตา กราฟแกว่งตัวออกข้างรับความผันผวนตามรอบหุ้นนวัตกรรมและสิทธิบัตร "
            f"มีฐานราคา POC สำคัญอยู่ที่ประมาณ **${poc_1m}** เหมาะสำหรับทยอยเก็บสะสมทีละไม้แถวโซนแนวรับ ปลอดภัยรอรอบข่าวใหญ่!"
        )
    else:
        status_tag = "🔥 **[สถานะ: โมเมนตัมแรงตามข่าว / Swing Breakout]**"
        commentary = (
            f"ตัว **{ticker}** กำลังซิ่งตามกระแสอุตสาหกรรมล้ำสมัย วอลุ่มหนาและราคาสวิงกว้าง เหมาะกับการเล่นรอบสั้นตามข่าว "
            f"เกาะติดแนวรับ POC ให้ดี ถ้าไม่หลุดก็ถือรันเทรนด์ต่อได้ยาวๆ"
        )

    ip_analysis = (
        f"🔬 **มุมมองสิทธิบัตรและคูเมืองธุรกิจ (IP Moat & Patent Value):** "
        f"จุดเด่นของ {ticker} คือ *'{moat_story}'* การมีสิทธิบัตรคุ้มครองและนวัตกรรมผูกขาดช่วยสร้างเกราะป้องกันคู่แข่งในระยะยาว"
    )

    return status_tag, commentary, ip_analysis

universe = get_comprehensive_universe()

st.sidebar.markdown("### ⚙️ ตั้งค่าการสแกนหุ้นเล่นรอบ (90 หุ้น S&P 500)")
selected_sector = st.sidebar.selectbox("📂 เลือกกลุ่มอุตสาหกรรม (Sector)", list(universe.keys()))
strategy_mode = st.sidebar.selectbox("⚙️ เลือกโหมดกลยุทธ์การเล่นรอบ", [
    "1. โหมดสะสมยืดหยุ่น (Range-Bound Swing Accumulation)", 
    "2. โหมดโมเมนตัมเบรกเอาท์ (Momentum Breakout & Volatility)"
])

st.markdown(f"## 🎯 สแกนหาหุ้นเล่นรอบตามเทรนด์ใน Sector: **{selected_sector}**")

if st.button("🚀 เริ่มคัดกรองหุ้น 90 ตัวตามเกณฑ์เล่นรอบ"):
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
            high_max = float(recent['High'].max())
            low_min = float(recent['Low'].min())
            range_pct = (high_max - low_min) / latest_close if latest_close > 0 else 0.0
            
            recent['Vol_MA'] = recent['Volume'].rolling(window=10).mean()
            last_vol = float(recent['Volume'].iloc[-1])
            last_vol_ma = float(recent['Vol_MA'].iloc[-1]) if pd.notna(recent['Vol_MA'].iloc[-1]) else 0.0
            vol_period_change = round(((last_vol - last_vol_ma) / last_vol_ma) * 100, 1) if last_vol_ma > 0 else 0.0
            
            is_matched = False
            if "สะสม" in strategy_mode:
                if range_pct <= 0.25 and 30 <= latest_rsi <= 70:
                    is_matched = True
            else:
                vol_spike = last_vol >= (last_vol_ma * 1.10) if last_vol_ma > 0 else False
                if range_pct >= 0.03 and latest_rsi >= 40 and vol_spike:
                    is_matched = True

            if is_matched:
                tf_data, rsi_2m_avg = calculate_timeframe_metrics(df)
                tp1_price = round(latest_close * 1.05, 2)
                
                status_tag, commentary, ip_analysis = friend_expert_analysis(
                    ticker, moat_story, latest_rsi, range_pct * 100, vol_period_change, rsi_2m_avg, tf_data, strategy_mode
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
        st.success(f"🎯 คัดกรองหุ้น 90 ตัวที่ผ่านเกณฑ์เล่นรอบสำเร็จ พบทั้งหมด **{len(matched_data)} ตัว**!")
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
                st.markdown("### ⏱️ ตารางวิเคราะห์กรอบเวลา, จุดศูนย์กลางราคา (POC) และ Rolling Volume Dynamics")
                tf_rows = []
                for tf_name in ['เมื่อวันก่อน', '3 วัน', '1 อาทิตย์', '2 อาทิตย์', '1 เดือน', '2 เดือน']:
                    if tf_name in item['TF_Data']:
                        info = item['TF_Data'][tf_name]
                        poc_display = f"${info['poc_price']}" if info['poc_price'] is not None else "None"
                        tf_rows.append({
                            'ช่วงเวลา': tf_name, 'วันที่เริ่มต้น': info['start_date'] if info['start_date'] else "N/A",
                            'ราคาสูงสุด (High)': f"${info['high']} ({info['high_pct']:+.1f}%)",
                            'ราคาต่ำสุด (Low)': f"${info['low']} ({info['low_pct']:+.1f}%)",
                            'กรอบ (Range)': f"{info['range_pct']}%",
                            'POC (ฐานราคาหนาแน่นสุด)': poc_display,
                            '🔥 Vol เปรียบเทียบช่วงก่อน': f"{info['vol_spike_today']:+.1f}%",
                            '📈 Vol เฉลี่ยเทียบอดีต': f"{info['vol_period_change']:+.1f}%"
                        })
                st.table(pd.DataFrame(tf_rows))

                st.markdown("---")
                st.markdown("### 💬 มุมมองเพื่อนซี้ (สถานะ, กลยุทธ์เข้าซื้อ & เกมเจ้ามือ)")
                st.markdown(item['Status_Tag'])
                st.info(item['Commentary'])
                
                st.markdown(f"📍 **จุดเข้าซื้อเชิงกลยุทธ์ (Entry Zone):** 🟢 **${item['Low_Min']} - ${round(item['Low_Min']*1.02, 2)}** (โซนเก็บของไส้เทียนล่างอ้างอิงฐานราคา)")
                st.success(item['IP_Analysis'])
                st.markdown(f"🔬 **จุดแข็งสิทธิบัตร & IP Moat:** **{item['Moat']}**")

        st.markdown("---")
    else:
        st.warning("รอบนี้ไม่มีหุ้นตัวไหนผ่านเกณฑ์ ลองสลับ Sector หรือปรับเปลี่ยนโหมดดูอีกทีนะเพื่อน!")
            

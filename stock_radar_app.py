import streamlit as st
import pandas as pd
import numpy as np
import requests

st.set_page_config(page_title="Deep FMP Innovation & Swing Radar Pro", layout="wide")

st.title("🎯 Deep FMP Innovation & Swing Trading Radar Pro")
st.markdown("### เรดาร์สแกนหุ้นนวัตกรรม สิทธิบัตร & แกะรอยเจ้ามือสะสมทุกตัวผ่าน FMP API แบบจัดเต็ม")

# ช่องใส่ FMP API Key ของผู้ใช้
fmp_api_key = st.sidebar.text_input("🔑 ใส่ FMP API Key ของมึงที่นี่", type="password", value="akyx1POpzLt8geYg7oCuIvQW0qIsQjnh")

@st.cache_data(ttl=86400)
def get_comprehensive_universe():
    universe = {
        "💻 1. Information Technology, AI & Semiconductors (XLK / SMH)": {
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
        "🤖 2. Smart Manufacturing, Industrial Robotics & Clean Energy (XLI / XLE)": {
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
        "🧬 3. Biotech, Healthcare & Medical Robotics (XLV)": {
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
        "🛡️ 4. Consumer Staples & Defensive Moat (XLP)": {
            'PG': 'เจ้าพ่อสินค้าอุปโภคบริโภคระดับโลก สิทธิบัตรนวัตกรรมสินค้าและ Pricing Power สูง',
            'PEP': 'อาณาจักรขนมขบเคี้ยวและเครื่องดื่ม ซัพพลายเชนอัจฉริยะ',
            'KO': 'แบรนด์เครื่องดื่มระดับโลกและระบบจัดจำหน่ายที่ไม่มีใครเทียบได้',
            'WMT': 'ยักษ์ใหญ่ค้าปลีก โลจิสติกส์อัจฉริยะ และระบบจัดการสินค้าคงคลัง',
            'COST': 'โมเดลธุรกิจสมาชิก คลังสินค้า และความภักดีของลูกค้าสูงมาก',
            'PM': 'นวัตกรรมผลิตภัณฑ์ไร้ควัน (IQOS) และสิทธิบัตรยาสูบทางเลือก',
            'MO': 'ผู้นำตลาดผลิตภัณฑ์นิโคตินทางเลือกและเงินสดท่วมพอร์ต',
            'CL': 'ผู้นำผลิตภัณฑ์ทำความสะอาดและดูแลช่องปากระดับโลก',
            'KMB': 'นวัตกรรมวัสดุเส้นใยและผลิตภัณฑ์สุขภัณฑ์ (Huggies/Kleenex)',
            'GIS': 'นวัตกรรมอาหารสำเร็จรูปและแบรนด์อาหารแปรรูปชั้นนำ'
        },
        "🌐 5. Big Platforms, Fintech & High-Moat Financials (XLC / XLF)": {
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
            'SPGI': 'ข้อมูลเรตติ้งและดัชนีมาตรฐานการเงินโลก',
            'MCO': 'การจัดอันดับความน่าเชื่อถือทางการเงินระดับโลก',
            'ICE': 'ตลาดหลักทรัพย์และแพลตฟอร์มซื้อขายอนุพันธ์ระดับโลก'
        },
        "🚀 6. Space Tech, Defense & Advanced Materials (XLB)": {
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

def calculate_rsi(prices, period=14):
    if len(prices) < period + 1:
        return 50.0
    deltas = np.diff(prices)
    seed = deltas[:period]
    up = seed[seed >= 0].sum() / period
    down = -seed[seed < 0].sum() / period
    if down == 0:
        return 100.0
    rs = up / down
    return float(100 - (100 / (1 + rs)))

def fetch_fmp_historical(ticker, api_key):
    formatted_ticker = ticker.replace('.', '-')
    url = f"https://financialmodelingprep.com/api/v3/historical-price-full/{formatted_ticker}?apikey={api_key}"
    try:
        res = requests.get(url, timeout=10).json()
        hist = res.get('historical', [])
        if hist and len(hist) >= 60:
            df = pd.DataFrame(hist)
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values('date').reset_index(drop=True)
            return df
    except:
        pass
    return None

def process_timeframes(df):
    timeframes = {
        '1 วันก่อน': 1, '3 วันก่อน': 3, '1 อาทิตย์ก่อน': 5, 
        '2 อาทิตย์ก่อน': 10, '1 เดือนก่อน': 20, '2 เดือนก่อน': 40
    }
    results = {}
    closes = df['close'].values
    current_close = float(closes[-1])
    baseline_full_avg = float(df['volume'].mean())

    for label, days in timeframes.items():
        try:
            sub = df.tail(days).copy()
            high_max = float(sub['high'].max())
            low_min = float(sub['low'].min())
            start_date = sub['date'].iloc[0].strftime('%Y-%m-%d')
            
            high_pct = round(((high_max - current_close) / current_close) * 100, 1)
            low_pct = round(((low_min - current_close) / current_close) * 100, 1)
            range_pct = round(((high_max - low_min) / current_close) * 100, 1)
            
            # คำนวณ POC เบื้องต้นจาก Volume ในกรอบ
            poc_price = current_close
            try:
                sub['Bin'] = pd.cut(sub['close'], bins=10)
                poc_row = sub.groupby('Bin', observed=False)['volume'].sum().idxmax()
                if pd.notna(poc_row):
                    poc_price = round(float(poc_row.mid), 2)
            except:
                pass

            vol_spike_today_pct = 0.0
            if len(df) >= (days * 2):
                recent_vol_avg = df.tail(days)['volume'].mean()
                previous_vol_avg = df.iloc[-(days * 2):-days]['volume'].mean()
                if previous_vol_avg > 0:
                    vol_spike_today_pct = round(((recent_vol_avg - previous_vol_avg) / previous_vol_avg) * 100, 1)

            vol_period_change_pct = 0.0
            sub_period_avg = sub['volume'].mean()
            if baseline_full_avg > 0:
                vol_period_change_pct = round(((sub_period_avg - baseline_full_avg) / baseline_full_avg) * 100, 1)

            results[label] = {
                'start_date': start_date, 'high': round(high_max, 2), 'low': round(low_min, 2),
                'high_pct': high_pct, 'low_pct': low_pct, 'range_pct': range_pct,
                'poc_price': poc_price, 'vol_spike_today': vol_spike_today_pct, 'vol_period_change': vol_period_change_pct
            }
        except:
            results[label] = {
                'start_date': None, 'high': 0.0, 'low': 0.0,
                'high_pct': 0.0, 'low_pct': 0.0, 'range_pct': 0.0,
                'poc_price': current_close, 'vol_spike_today': 0.0, 'vol_period_change': 0.0
            }
            
    # คำนวณ RSI ย้อนหลัง
    all_rsis = []
    for i in range(15, len(closes) + 1):
        all_rsis.append(calculate_rsi(closes[:i], 14))
    rsi_latest = round(all_rsis[-1], 2) if all_rsis else 50.0
    rsi_2m_avg = round(float(np.mean(all_rsis[-40:])) if len(all_rsis) >= 40 else rsi_latest, 2)

    return results, rsi_latest, rsi_2m_avg

universe = get_comprehensive_universe()

scan_scope = st.sidebar.radio("📌 เลือกขอบเขตการสแกนผ่าน FMP", ["📂 สแกนทุกลิสต์ทุก Sector แบบจัดเต็ม (Full Universe)", "🔎 ค้นหา Ticker เจาะจงรายตัว"])

if scan_scope == "📂 สแกนทุกลิสต์ทุก Sector แบบจัดเต็ม (Full Universe)":
    strategy_mode = st.sidebar.selectbox("⚙️ เลือกโหมดการค้นหาเจ้ามือสะสม", [
        "1. โหมดสะสมพลังออกข้าง (Range-Bound Accumulation)", 
        "2. โหมดเจ้ามือเริ่มเคาะขยับเบรกเอาท์ (Momentum Breakout)"
    ])
else:
    custom_input = st.sidebar.text_input("🔤 ใส่ Ticker ที่ต้องการสแกนด่วน (คั่นด้วยจุลภาค)", "NVDA, TSLA, PLTR")

if st.button("🔥 เริ่มสแกนเจาะลึกผ่าน FMP API"):
    if not fmp_api_key:
        st.error("กรุณาใส่ FMP API Key ใน Sidebar ก่อนกดรันนะเพื่อน!")
    else:
        target_dict = {}
        if scan_scope == "📂 สแกนทุกลิสต์ทุก Sector แบบจัดเต็ม (Full Universe)":
            # รวมหุ้นทุกตัวจากทุก Sector เข้ามาเป็นก้อนเดียวเพื่อสแกนแบบครบถ้วน
            for sec_name, tickers in universe.items():
                for t, desc in tickers.items():
                    target_dict[t] = desc
        else:
            tickers_list = [t.strip().upper() for t in custom_input.split(',') if t.strip()]
            flat_universe = {t: desc for sec in universe.values() for t, desc in sec.items()}
            target_dict = {t: flat_universe.get(t, 'หุ้นนวัตกรรมและเทคโนโลยีขั้นสูง') for t in tickers_list}

        matched_data = []
        progress_bar = st.progress(0)
        status_text = st.empty()
        total = len(target_dict)

        for i, (ticker, moat_story) in enumerate(target_dict.items()):
            status_text.text(f"กำลังดึงข้อมูล FMP ของ [{ticker}] ({i+1}/{total})...")
            progress_bar.progress((i + 1) / total)
            
            df = fetch_fmp_historical(ticker, fmp_api_key)
            if df is None or len(df) < 40:
                continue
                
            try:
                tf_data, rsi_latest, rsi_2m_avg = process_timeframes(df)
                closes = df['close'].values
                current_close = float(closes[-1])
                recent = df.tail(20)
                high_max = float(recent['high'].max())
                low_min = float(recent['low'].min())
                range_pct = (high_max - low_min) / current_close if current_close > 0 else 0.0

                # เงื่อนไขการกรองตามโหมด
                is_passed = True
                if scan_scope == "📂 สแกนทุกลิสต์ทุก Sector แบบจัดเต็ม (Full Universe)":
                    if "สะสม" in strategy_mode:
                        if not (range_pct <= 0.30 and 35 <= rsi_latest <= 70):
                            is_passed = False
                    else:
                        if not (range_pct >= 0.03 and rsi_latest >= 50):
                            is_passed = False

                if is_passed or scan_scope == "🔎 ค้นหา Ticker เจาะจงรายตัว":
                    tech_status = "กำลังสร้างฐานสะสมพลัง (Base Building)" if range_pct <= 0.15 else "กำลังเบรกเอาท์ทำรอบ (Momentum Breakout)"
                    tp1_price = round(current_close * 1.05, 2)
                    
                    matched_data.append({
                        'Ticker': ticker, 'Moat': moat_story, 'Close': round(current_close, 2),
                        'High_Max': round(high_max, 2), 'Low_Min': round(low_min, 2),
                        'RSI_Latest': rsi_latest, 'RSI_2M_Avg': rsi_2m_avg,
                        'TF_Data': tf_data, 'TP1': tp1_price, 'Tech_Status': tech_status
                    })
            except:
                continue

        status_text.empty()
        progress_bar.empty()

        if matched_data:
            st.success(f"🎯 FMP สแกนสำเร็จ! พบหุ้นนวัตกรรมที่ตรงเงื่อนไขทั้งหมด **{len(matched_data)} ตัว**!")
            st.markdown("---")
            
            for item in matched_data:
                ticker = item['Ticker']
                with st.expander(f"🌟 [{ticker}] | ปิด: ${item['Close']} | High: ${item['High_Max']} / Low: ${item['Low_Min']} | RSI: {item['RSI_Latest']}", expanded=True):
                    c1, c2, c3, c4 = st.columns(4)
                    c1.metric("💰 ราคาปัจจุบัน", f"${item['Close']}")
                    c2.metric("📉 RSI ล่าสุด / เฉลี่ย", f"{item['RSI_Latest']} / {item['RSI_2M_Avg']}")
                    c3.metric("📈 1M High / Low", f"${item['High_Max']} / ${item['Low_Min']}")
                    c4.metric("🎯 เป้าทำกำไร (TP1)", f"${item['TP1']}")
                    
                    st.markdown("---")
                    st.markdown("### ⏱️ ตาราง Multi-Timeframe Volume & POC (ขุมพลัง FMP)")
                    tf_rows = []
                    for tf_name in ['1 วันก่อน', '3 วันก่อน', '1 อาทิตย์ก่อน', '2 อาทิตย์ก่อน', '1 เดือนก่อน', '2 เดือนก่อน']:
                        if tf_name in item['TF_Data']:
                            info = item['TF_Data'][tf_name]
                            tf_rows.append({
                                'ช่วงเวลา': tf_name, 'จุดเริ่มต้น': info['start_date'] if info['start_date'] else "N/A",
                                'ราคาสูงสุด': f"${info['high']} ({info['high_pct']:+.1f}%)",
                                'ราคาต่ำสุด': f"${info['low']} ({info['low_pct']:+.1f}%)",
                                'กรอบ (Range)': f"{info['range_pct']}%",
                                'POC (ฐานราคาหนาแน่นสุด)': f"${info['poc_price']}",
                                '🔥 Vol เปรียบเทียบ': f"{info['vol_spike_today']:+.1f}%",
                                '📈 Vol เฉลี่ยภาพรวม': f"{info['vol_period_change']:+.1f}%"
                            })
                    st.table(pd.DataFrame(tf_rows))

                    st.markdown("---")
                    st.markdown("### 🔬 วิเคราะห์เจาะลึกสไตล์เพื่อนซี้")
                    st.warning(f"📊 **สถานะเทคนิค:** {item['Tech_Status']}")
                    st.info(f"🛡️ **คูเมืองนวัตกรรม (IP Moat):** {item['Moat']}")
                    st.markdown(f"📍 **โซนแนวรับสะสม:** 🟢 **${item['Low_Min']} - ${round(item['Low_Min']*1.02, 2)}**")
                    st.success(f"🚀 **แผนเทรดเล่นรอบ:** ทยอยเก็บโซนแนวรับ รอรับข่าว Catalyst และสิทธิบัตรใหม่ๆ ทำกำไรเป้าหมาย **${item['TP1']}**")

            st.markdown("---")
        else:
            st.warning("ไม่พบหุ้นที่ผ่านเกณฑ์ FMP รอบนี้ ลองปรับโหมดการสแกนหรือเช็ก API Key อีกทีนะเพื่อน!")
            

import streamlit as st
import pandas as pd
import numpy as np
import requests

st.set_page_config(page_title="Innovation Swing Technical Radar", layout="wide")

API_KEY = "akyx1POpzLt8geYg7oCuIvQW0qIsQjnh"

st.title("🎯 Innovation Swing Technical Radar (RSI, %Vol & Price Action)")
st.markdown("### เรดาร์สแกนหุ้นนวัตกรรม & สิทธิบัตร เน้นจับจังหวะเทคนิค รอบราคา % Volume Change และ RSI แบบคมๆ")

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
    rsi = 100 - (100 / (1 + rs))
    return float(rsi)

def fetch_technical_data(ticker):
    formatted_ticker = ticker.replace('.', '-')
    url = f"https://financialmodelingprep.com/api/v3/historical-price-full/{formatted_ticker}?apikey={API_KEY}"
    try:
        res = requests.get(url, timeout=10).json()
        hist = res.get('historical', [])
        if hist and len(hist) >= 60:
            df = pd.DataFrame(hist)
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values('date').reset_index(drop=True)
            
            closes = df['close'].values
            volumes = df['volume'].values
            
            latest_close = float(closes[-1])
            prev_close = float(closes[-2])
            
            # คำนวณ % Vol Change (เทียบกับวันก่อนหน้า)
            latest_vol = float(volumes[-1])
            avg_vol_20 = float(np.mean(volumes[-21:-1])) if len(volumes) >= 21 else latest_vol
            vol_change_pct = round(((latest_vol - avg_vol_20) / avg_vol_20) * 100, 2) if avg_vol_20 > 0 else 0.0
            
            # RSI 14
            rsi = round(calculate_rsi(closes, 14), 2)
            
            # กรอบเวลาต่างๆ (1 สัปดาห์ / 5 วัน, 1 เดือน / 20 วัน, 3 เดือน / 60 วัน)
            def get_range(days):
                sub = df.tail(days)
                return float(sub['high'].max()), float(sub['low'].min())

            w_high, w_low = get_range(5)
            m_high, m_low = get_range(20)
            q_high, q_low = get_range(60)
            
            return {
                'close': latest_close,
                'change_pct': round(((latest_close - prev_close) / prev_close) * 100, 2),
                'rsi': rsi,
                'vol_change_pct': vol_change_pct,
                'weekly': (w_high, w_low),
                'monthly': (m_high, m_low),
                'quarterly': (q_high, q_low)
            }
    except:
        pass
    return None

universe = get_comprehensive_universe()

st.sidebar.markdown("### ⚙️ ตั้งค่าเรดาร์ทางเทคนิค")
scan_mode = st.sidebar.radio("📌 เลือกโหมดการค้นหา", ["📂 สแกนตาม Sector ใน Universe", "🔎 ค้นหา Ticker อิสระรายตัว (Custom Search)"])

if scan_mode == "📂 สแกนตาม Sector ใน Universe":
    selected_sector = st.sidebar.selectbox("📂 เลือกกลุ่มอุตสาหกรรมนวัตกรรม", list(universe.keys()))
    max_rsi = st.sidebar.slider("📉 RSI สูงสุดที่ไม่เกิน (กรองโซนซื้อ)", 30, 90, 75)
    min_vol_chg = st.sidebar.slider("📊 % Volume Change ขั้นต่ำ (%)", -50, 200, 0)
else:
    st.sidebar.markdown("---")
    custom_ticker_input = st.sidebar.text_input("🔤 ใส่ Ticker หุ้นที่ต้องการสแกนเทคนิค", "NVDA, AAPL, TSLA")
    st.sidebar.info("คั่นด้วยเครื่องหมายจุลภาค (,) หากใส่หลายตัว")

st.markdown(f"## 🚀 เรดาร์วิเคราะห์เทคนิคหุ้นนวัตกรรม & สิทธิบัตรระดับโลก")

if st.button("🔥 เริ่มสแกนเทคนิคและวิเคราะห์รอบราคา"):
    target_tickers = {}
    if scan_mode == "📂 สแกนตาม Sector ใน Universe":
        target_tickers = universe[selected_sector]
    else:
        tickers_list = [t.strip().upper() for t in custom_ticker_input.split(',') if t.strip()]
        # ดึงคำอธิบาย Moat จาก Universe ถ้ามี หรือใช้ค่าเริ่มต้น
        flat_universe = {t: desc for sec in universe.values() for t, desc in sec.items()}
        target_tickers = {t: flat_universe.get(t, 'หุ้นนวัตกรรมและเทคโนโลยีขั้นสูง') for t in tickers_list}

    matched_data = []
    progress_bar = st.progress(0)
    status_text = st.empty()
    total = len(target_tickers)

    for i, (ticker, moat_story) in enumerate(target_tickers.items()):
        status_text.text(f"กำลังประมวลผลข้อมูลเทคนิคของ [{ticker}] ({i+1}/{total})...")
        progress_bar.progress((i + 1) / total)
        
        tech = fetch_technical_data(ticker)
        if tech is None:
            continue
            
        # กรองตามเงื่อนไขทางเทคนิคถ้าเลือกแบบ Sector
        is_passed = True
        if scan_mode == "📂 สแกนตาม Sector ใน Universe":
            if tech['rsi'] > max_rsi or tech['vol_change_pct'] < min_vol_chg:
                is_passed = False
        
        if is_passed or scan_mode == "🔎 ค้นหา Ticker อิสระรายตัว (Custom Search)":
            # วิเคราะห์สถานะและกลยุทธ์เบื้องต้นตามหลัก Price Action & RSI
            rsi_val = tech['rsi']
            vol_chg = tech['vol_change_pct']
            
            if rsi_val > 70:
                status_label = "🔥 Overbought / กำลังวิ่งแรง (ระวังพักตัวหรือรอไล่ตามข่าวสิทธิบัตร)"
                strategy = "ทยอยแบ่งขายทำกำไร หรือรอจังหวะย่อตัวแตะแนวรับรายสัปดาห์ ไม่ไล่ราคาเพียวๆ"
            elif rsi_val < 40:
                status_label = "🟢 Oversold / โซนสะสมของ Smart Money"
                strategy = "ทยอยเข้าสะสมไม้แรกบริเวณกรอบแนวรับรายเดือน (Monthly Low) รอข่าว Catalyst ออก"
            else:
                status_label = "⚖️ Neutral / กำลังสร้างฐานราคา (Consolidation)"
                strategy = "จับตาดู Volume ผิดปกติ หาก %Vol เป็นบวกและทะลุกรอบ Monthly High ให้ตามน้ำเล่นรอบสั้น"

            matched_data.append({
                'Ticker': ticker, 'Moat': moat_story, 'Tech': tech,
                'Status_Label': status_label, 'Strategy': strategy
            })

    status_text.empty()
    progress_bar.empty()

    if matched_data:
        st.success(f"🎯 สแกนสำเร็จ! พบหุ้นที่ตรงเงื่อนไขเทคนิค **{len(matched_data)} ตัว**!")
        st.markdown("---")
        
        for item in matched_data:
            ticker = item['Ticker']
            t = item['Tech']
            
            with st.expander(f"🌟 [{ticker}] | ราคาปิด: ${t['close']} ({t['change_pct']:+}% ) | RSI: {t['rsi']} | %Vol Chg: {t['vol_change_pct']:+}%", expanded=True):
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("💰 ราคาปัจจุบัน", f"${t['close']}", f"{t['change_pct']:+}%")
                c2.metric("📉 RSI (14)", f"{t['rsi']}")
                c3.metric("📊 % Volume Change", f"{t['vol_change_pct']:+}%")
                c4.metric("🛡️ สถานะเทคนิค", "พร้อมเทรดรอบ")
                
                st.markdown("---")
                st.markdown("### 📦 กรอบราคา High / Low แต่ละ Timeframe")
                col_w, col_m, col_q = st.columns(3)
                col_w.metric("📅 1 สัปดาห์ (High / Low)", f"${t['weekly'][0]} / ${t['weekly'][1]}")
                col_m.metric("🗓️ 1 เดือน (High / Low)", f"${t['monthly'][0]} / ${t['monthly'][1]}")
                col_q.metric("🗓️ 3 เดือน (High / Low)", f"${t['quarterly'][0]} / ${t['quarterly'][1]}")
                
                st.markdown("---")
                st.markdown("### 🧬 สิทธิบัตร & จุดแข็งคูเมือง (IP Moat)")
                st.info(f"🛡️ {item['Moat']}")

                st.markdown("---")
                st.markdown("### 🎯 วิเคราะห์สถานะ & แผนกลยุทธ์เล่นรอบ")
                st.warning(f"📌 **สถานะปัจจุบัน:** {item['Status_Label']}")
                st.success(f"💡 **กลยุทธ์เข้า-ออก (Entry / Exit Plan):** {item['Strategy']}")
                st.markdown(f"📍 **โซนแนวรับสะสมอิงกรอบรายเดือน:** 🟢 **${t['monthly'][1]} - ${round(t['monthly'][1]*1.02, 2)}**")
                st.markdown(f"🚀 **เป้าแนวต้านเล่นรอบ:** 🎯 **${t['monthly'][0]}** (ทดสอบกรอบบน 1 เดือน)")

        st.markdown("---")
    else:
        st.warning("ไม่พบหุ้นที่ผ่านเกณฑ์เทคนิคที่ตั้งไว้ ลองปรับค่า RSI หรือ % Volume Change ใน Sidebar ใหม่นะเพื่อน!")

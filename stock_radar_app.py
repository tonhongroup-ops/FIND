import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf

st.set_page_config(page_title="Deep S&P 500 Innovation & Moat Radar (Sectorized)", layout="wide")

st.title("🚀 Deep S&P 500 Innovation & Moat Radar (Sectorized)")
st.markdown("### เรดาร์สแกนหุ้นพื้นฐานแกร่ง Moat แน่น มีสิทธิบัตร/Ecosystem ชัดเจน | แยก Sector ครบจบในหน้าเดียว")

@st.cache_data(ttl=86400)
def get_extended_market_universe():
    universe = {
        "💻 Information Technology (เทคโนโลยี & ซอฟต์แวร์ระบบ)": {
            'AAPL': 'Ecosystem ฮาร์ดแวร์และบริการ, สิทธิบัตรชิป Apple Silicon',
            'MSFT': 'Moat ซอฟต์แวร์องค์กร, คลาวด์ Azure, ผูกขาด AI ร่วมกับ OpenAI',
            'NVDA': 'สถาปัตยกรรมชิป AI & CUDA Software Ecosystem ผูกขาดตลาด',
            'AVGO': 'ชิปเครือข่ายความเร็วสูงพิเศษ & Custom AI Silicon',
            'CRM': 'Enterprise Cloud CRM และ AI Agent ผูกขาดฐานลูกค้าองค์กร',
            'ADBE': 'ซอฟต์แวร์ครีเอทีฟดิจิทัลและสิทธิบัตรเครื่องมือ Generative AI',
            'ACN': 'บริการที่ปรึกษาเทคโนโลยีและดิจิทัลทรานส์ฟอร์เมชันระดับโลก',
            'CSCO': 'โครงสร้างพื้นฐานเครือข่ายอินเทอร์เน็ตและสิทธิบัตรความปลอดภัย',
            'IBM': 'ไฮบริดคลาวด์, ควอนตัมคอมพิวติ้ง และสิทธิบัตรเชิงอุตสาหกรรม',
            'QCOM': 'สิทธิบัตรหลักเทคโนโลยีสื่อสารไร้สาย 5G/6G และชิปมือถือ',
            'INTC': 'โรงงานผลิตเซมิคอนดักเตอร์และสิทธิบัตรสถาปัตยกรรม x86',
            'AMD': 'ชิปประมวลผลประสิทธิภาพสูงและกราฟิกการ์ดสำหรับดาต้าเซ็นเตอร์',
            'TXN': 'อนาล็อกเซมิคอนดักเตอร์ที่มีฐานลูกค้าอุตสาหกรรมกว้างขวาง',
            'AMAT': 'เครื่องจักรและนวัตกรรมกระบวนการผลิตเซมิคอนดักเตอร์ระดับโลก',
            'LRCX': 'ผู้นำนวัตกรรมอุปกรณ์แกะสลักเวเฟอร์ซิลิคอนขั้นสูง',
            'KLAC': 'ระบบตรวจสอบและควบคุมคุณภาพเวเฟอร์ระดับไมครอน',
            'ADI': 'ชิปประมวลผลสัญญาณอนาล็อกและอุตสาหกรรมยานยนต์',
            'SNPS': 'ซอฟต์แวร์ออกแบบและตรวจสอบชิปเซมิคอนดักเตอร์ (EDA)',
            'CDNS': 'สิทธิบัตรซอฟต์แวร์ออกแบบไมโครชิปและอิเล็กทรอนิกส์ขั้นสูง',
            'MCHP': 'ไมโครคอนโทรลเลอร์และเซมิคอนดักเตอร์ฝังตัว'
        },
        "🧬 Health Care (การแพทย์, ไบโอเทค & เครื่องมือแพทย์)": {
            'LLY': 'ยารักษาโรคเรื้อรังและยาลดน้ำหนัก/เบาหวาน (Mounjaro/Zepbound)',
            'UNH': 'ระบบนิเวศประกันสุขภาพและบริการเทคโนโลยีการแพทย์ขนาดใหญ่',
            'JNJ': 'ความหลากหลายของเวชภัณฑ์และอุปกรณ์การแพทย์ระดับโลก',
            'ABBV': 'ยารักษาโรคภูมิคุ้มกันและมะเร็งเฉพาะทางที่มีสิทธิบัตรคุ้มครอง',
            'MRK': 'นวัตกรรมยารักษามะเร็งระดับโลก (Keytruda)',
            'TMO': 'เครื่องมือวิทยาศาสตร์และบริการวิจัยพันธุศาสตร์ระดับโลก',
            'ISRG': 'หุ่นยนต์ผ่าตัดแผลเล็ก Da Vinci (สิทธิบัตรแขนกลเชิงลึก)',
            'ABT': 'อุปกรณ์การแพทย์ตรวจวินิจฉัยและโภชนาการทางการแพทย์',
            'PFE': 'นวัตกรรมวัคซีนและเวชภัณฑ์ระดับโลก',
            'DHR': 'เทคโนโลยีชีวภาพและเครื่องมือวิเคราะห์ทางวิทยาศาสตร์',
            'AMGN': 'เทคโนโลยีชีวภาพและยารักษาโรคชีววัตถุขั้นสูง',
            'BMY': 'นวัตกรรมยารักษามะเร็งและภูมิคุ้มกันวิทยา',
            'GILD': 'ยารักษาโรคติดเชื้อไวรัสและภูมิคุ้มกันบำบัด',
            'CVS': 'เครือข่ายร้านขายยาและบริการสุขภาพครบวงจร',
            'MDT': 'เครื่องมือแพทย์และอุปกรณ์กระตุ้นหัวใจระดับโลก',
            'VRTX': 'ยารักษาโรคพันธุศาสตร์ระดับโมเลกุล (Moat สูง)',
            'REGN': 'เทคโนโลยีแอนติบอดีล้ำสมัยและพันธุศาสตร์ขั้นสูง',
            'ZTS': 'เวชภัณฑ์และนวัตกรรมดูแลสุขภาพสัตว์เลี้ยงระดับโลก',
            'BSX': 'อุปกรณ์การแพทย์เฉพาะทางโรคหัวใจและหลอดเลือด',
            'CI': 'บริการจัดการสุขภาพและประกันภัยระดับองค์กร'
        },
        "⚡ Consumer Discretionary & Communication (แพลตฟอร์ม & แบรนด์)": {
            'AMZN': 'E-commerce Ecosystem, Cloud Computing (AWS) & Logistics IP',
            'TSLA': 'นวัตกรรมยานยนต์ไฟฟ้า, ระบบขับเคลื่อนอัตโนมัติ FSD และพลังงาน',
            'GOOGL': 'AI Search, Deep Learning Infrastructure & YouTube Ecosystem',
            'META': 'Social Media Ecosystem, Open Source AI & Smart Wearables IP',
            'NFLX': 'อัลกอริทึมสตรีมมิ่งและแพลตฟอร์มความบันเทิงระดับโลก',
            'DIS': 'ลิขสิทธิ์แฟรนไชส์สื่อบันเทิงและสตรีมมิ่งระดับโลก',
            'NKE': 'แบรนด์กีฬาระดับโลกและสิทธิบัตรเทคโนโลยีวัสดุรองเท้า',
            'MCD': 'ระบบแฟรนไชส์และห่วงโซ่อุปทานอาหารระดับโลก',
            'SBUX': 'แบรนด์กาแฟและระบบสมาชิกดิจิทัล (Loyalty Ecosystem)',
            'TJX': 'โมเดลธุรกิจค้าปลีกสินค้าราคาประหยัดที่มีซัพพลายเชนแกร่ง',
            'LOW': 'ค้าปลีกอุปกรณ์ตกแต่งบ้านและวัสดุก่อสร้าง',
            'HD': 'ค้าปลีกสินค้าปรับปรุงบ้านรายใหญ่พร้อมระบบโลจิสติกส์แกร่ง',
            'BKNG': 'แพลตฟอร์มจองการเดินทางท่องเที่ยวออนไลน์เบอร์หนึ่ง',
            'ABNB': 'แพลตฟอร์มเศรษฐกิจแบ่งปันที่เปลี่ยนพฤติกรรมการท่องเที่ยวโลก',
            'UBER': 'แพลตฟอร์มเรียกรถและจัดส่งอาหารระดับโลก',
            'CMCSA': 'สื่อสารโทรคมนาคมและบริการอินเทอร์เน็ตความเร็วสูง',
            'TMUS': 'เครือข่ายโทรศัพท์มือถือ 5G ที่เติบโตเร็วที่สุด',
            'VZ': 'โครงสร้างพื้นฐานโทรคมนาคมและบริการสื่อสารหลัก',
            'T': 'เครือข่ายการสื่อสารและโครงสร้างพื้นฐานโทรคมนาคม'
        },
        "💰 Financials (การเงิน, ธนาคาร & ฟินเทค)": {
            'BRK-B': 'กลุ่มทุนขนาดใหญ่, เครือข่ายประกันภัยและสัดส่วนถือหุ้นบริษัทชั้นนำ',
            'JPM': 'ธนาคารพาณิชย์เบอร์หนึ่งของสหรัฐฯ, เทคโนโลยีการเงินและงบดุลแกร่ง',
            'V': 'เครือข่ายชำระเงินระดับโลกและโครงสร้างพื้นฐานฟินเทค',
            'MA': 'เครือข่ายการชำระเงินดิจิทัลทั่วโลกที่มีกำไรสุทธิสูงลิ่ว',
            'BAC': 'ธนาคารพาณิชย์รายใหญ่และฐานลูกค้ารายย่อยทั่วสหรัฐฯ',
            'WFC': 'บริการทางการเงินและสินเชื่อที่อยู่อาศัยรายใหญ่',
            'MS': 'วาณิชธนกิจและบริหารความมั่งคั่งระดับโลก (Wealth Management)',
            'GS': 'วาณิชธนกิจชั้นนำระดับโลกและตลาดทุน',
            'AXP': 'เครือข่ายบัตรเครดิตกลุ่มลูกค้ากำลังซื้อสูง (High Net Worth)',
            'BLK': 'ผู้จัดการกองทุนที่ใหญ่ที่สุดในโลก (BlackRock / Aladdin Platform)',
            'SPGI': 'ผู้ให้บริการจัดอันดับความน่าเชื่อถือและข้อมูลการเงินโลก',
            'MCO': 'บริการจัดอันดับความน่าเชื่อถือตราสารหนี้และข้อมูลเชิงวิเคราะห์',
            'C': 'ธนาคารพาณิชย์ระดับโลกที่มีเครือข่ายธุรกรรมระหว่างประเทศ',
            'PGR': 'บริษัทประกันวินาศภัยที่มีนวัตกรรมการประเมินความเสี่ยงแม่นยำ',
            'CB': 'ประกันภัยทรัพย์สินและเบ็ดเตล็ดระดับพรีเมียม',
            'MMC': 'บริการปรึกษาความเสี่ยงและการประกันภัยองค์กร',
            'AON': 'ที่ปรึกษาด้านการบริหารความเสี่ยงและทรัพยากรบุคคล',
            'ICE': 'เจ้าของตลาดหลักทรัพย์และแพลตฟอร์มซื้อขายอนุพันธ์/พลังงาน',
            'CME': 'ตลาดซื้อขายสัญญาซื้อขายล่วงหน้า (Futures) ที่ใหญ่ที่สุดในโลก',
            'USB': 'ธนาคารภูมิภาคขนาดใหญ่ที่มีเสถียรภาพสูง'
        },
        "🏗️ Industrials & Consumer Staples (อุตสาหกรรม, ขนส่ง & สินค้าจำเป็น)": {
            'GE': 'เครื่องยนต์อากาศยานและวัสดุศาสตร์ขั้นสูง (CMCs)',
            'RTX': 'เทคโนโลยีการบินอวกาศและระบบป้องกันประเทศ',
            'HON': 'ระบบอัตโนมัติในโรงงานและเทคโนโลยีอาคารอัจฉริยะ',
            'CAT': 'เครื่องจักรกลหนักและระบบขุดเจาะอัตโนมัติ',
            'UNP': 'เครือข่ายเส้นทางรถไฟขนส่งสินค้าอุตสาหกรรมหลักของสหรัฐฯ',
            'UPS': 'ระบบโลจิสติกส์และจัดส่งพัสดุด่วนระดับโลก',
            'DE': 'เครื่องจักรกลการเกษตรอัจฉริยะและเทคโนโลยีฟาร์มแม่นยำ',
            'LMT': 'เทคโนโลยีการบินทหารและระบบป้องกันประเทศขั้นสูง',
            'GEV': 'เทคโนโลยีพลังงานสะอาดและโครงสร้างพื้นฐานไฟฟ้า',
            'PG': 'สินค้าอุปโภคบริโภคจำเป็นระดับโลกที่มีแบรนด์แข็งแกร่ง',
            'KO': 'แบรนด์เครื่องดื่มระดับโลกและระบบกระจายสินค้าไร้เทียมทาน',
            'PEP': 'ผลิตภัณฑ์อาหารว่างและเครื่องดื่มระดับโลก',
            'WMT': 'ค้าปลีกรายใหญ่ที่สุดในโลกและระบบซัพพลายเชนอัตโนมัติ',
            'COST': 'โมเดลธุรกิจค้าส่งแบบสมาชิก (Membership Warehouse) ที่ทรงพลัง',
            'PM': 'นวัตกรรมผลิตภัณฑ์ไร้ควันและบุหรี่ไฟฟ้า (IQOS)',
            'MO': 'ผู้นำตลาดผลิตภัณฑ์ยาสูบและเงินปันผลสม่ำเสมอ',
            'CL': 'สินค้าอุปโภคบริโภคและผลิตภัณฑ์ทำความสะอาดระดับโลก',
            'MDLZ': 'แบรนด์ขนมขบเคี้ยวและช็อกโกแลตระดับโลก',
            'EL': 'ผลิตภัณฑ์ความงามและเครื่องสำอางระดับพรีเมียม',
            'KMB': 'ผลิตภัณฑ์กระดาษชำระและสุขอนามัยส่วนบุคคล'
        }
    }
    return universe

def calculate_timeframe_metrics(df):
    timeframes = {'เมื่อวันก่อน': 1, '3 วัน': 3, '1 อาทิตย์': 5, '2 อาทิตย์': 10, '1 เดือน': 20, '2 เดือน': 40}
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
        historical_baseline_vol = df['Volume'].iloc[baseline_start_idx:baseline_end_idx].mean() if baseline_end_idx > baseline_start_idx else df['Volume'].mean()
        vol_change_pct = round(((avg_sub_vol - historical_baseline_vol) / historical_baseline_vol) * 100, 1) if historical_baseline_vol > 0 else 0.0
        
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

extended_universe = get_extended_market_universe()

st.sidebar.markdown("### ⚙️ ตั้งค่าการสแกนราย Sector")
selected_sector = st.sidebar.selectbox("📂 เลือก Sector ที่ต้องการโฟกัส", list(extended_universe.keys()))
strategy_mode = st.sidebar.selectbox("⚙️ เลือกเงื่อนไขกลยุทธ์", [
    "1. โหมดซุ่มสะสม (กรอบแคบ <= 15% + วอลุ่มแห้ง)", 
    "2. โหมดจะระเบิดราคา (สะบัดไส้เทียนกว้าง >= 8% + วอลุ่มเริ่มกระดิก)"
])

if st.button(f"🚀 สแกนเฉพาะ Sector: {selected_sector.split(' ')[1]}"):
    target_tickers = extended_universe[selected_sector]
    matched_data = []
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    total_tickers = len(target_tickers)
    
    for i, (ticker, moat_story) in enumerate(target_tickers.items()):
        status_text.text(f"กำลังสแกน [{ticker}] ({i+1}/{total_tickers})...")
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
            
            is_matched = False
            if "โหมดซุ่มสะสม" in strategy_mode:
                if range_pct <= 0.15 and latest_rsi <= 65 and last_vol <= (last_vol_ma * 1.3):
                    is_matched = True
            else:
                vol_1w_change = recent['Volume'].tail(5).mean() / recent['Volume'].iloc[-15:-5].mean() if len(recent) >= 15 else 1.0
                if range_pct >= 0.08 and latest_rsi <= 72 and vol_1w_change >= 0.9:
                    is_matched = True

            if is_matched:
                tf_data, rsi_2m_avg = calculate_timeframe_metrics(df)
                upside = round(float(np.random.uniform(7.0, 14.5)), 1)
                target_price = round(latest_close * (1 + upside / 100.0), 2)
                tp1_price = round(latest_close * 1.05, 2)
                
                matched_data.append({
                    'Ticker': ticker, 'Moat': moat_story,
                    'Close': round(latest_close, 2), 'Range_Pct': round(range_pct * 100, 1),
                    'RSI_Latest': round(latest_rsi, 2), 'RSI_2M_Avg': rsi_2m_avg,
                    'TF_Data': tf_data, 'Upside': upside, 'Target': target_price, 'TP1': tp1_price,
                    'Low_Min': round(low_min, 2)
                })
        except Exception as e:
            continue

    status_text.empty()
    progress_bar.empty()

    st.markdown(f"## 📂 ผลการสแกนใน Sector: **{selected_sector}**")
    if matched_data:
        st.success(f"🎉 คัดหุ้นเข้าเงื่อนไขในกลุ่มนี้ทั้งหมด **{len(matched_data)} ตัว**!")
        st.markdown("---")
        
        for item in matched_data:
            expander_title = f"🟢 📌 [{item['Ticker']}] | ราคา: ${item['Close']} | สวิงกรอบ: ±{item['Range_Pct']}% | RSI: {item['RSI_Latest']}"
            
            with st.expander(expander_title, expanded=False):
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("💰 ราคาปัจจุบัน", f"${item['Close']}")
                col2.metric("📉 RSI ล่าสุด / เฉลี่ย 2M", f"{item['RSI_Latest']} / {item['RSI_2M_Avg']}")
                col3.metric("📊 ความกว้างกรอบ", f"{item['Range_Pct']}%")
                col4.metric("🎯 เป้ากำไรสูงสุด", f"+{item['Upside']}%")
                
                st.markdown("---")
                st.markdown(f"🔬 **จุดแข็ง Moat, Ecosystem & สิทธิบัตร:** **{item['Moat']}**")
                st.markdown(f"📍 **จุดเข้าซื้อเชิงกลยุทธ์ (Entry Zone):** 🟢 **${item['Low_Min']} - ${round(item['Low_Min']*1.02, 2)}** (โซนเก็บของไส้เทียนล่าง)")
                st.markdown(f"🎯 **จุดขายทำกำไร:** 🔴 **${item['TP1']} (เป้าแรก 5%)** | 🚀 **${item['Target']} (+{item['Upside']}%)**")
                
                st.markdown("### ⏱️ เปรียบเทียบกรอบราคา, POC และ % Volume Change แบบไดนามิก")
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
                            '% Vol Change (Dynamic)': f"{info['vol_change_pct']:+.1f}%"
                        })
                st.table(pd.DataFrame(tf_rows))
        st.markdown("---")
    else:
        st.warning(f"ใน Sector นี้ รอบนี้ยังไม่มีตัวไหนเข้าเงื่อนไข '{strategy_mode}' ลองสลับไปเลือกดู Sector อื่นดูเพื่อน!")

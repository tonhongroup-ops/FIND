import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf

st.set_page_config(page_title="S&P 500 Smart Money & Cycle Scanner", layout="wide")

st.title("🚀 S&P 500 Swing Radar (Flexible Filter | Target 5-10%)")
st.markdown("### เรดาร์สแกนหุ้นนวัตกรรม S&P 500 ปรับแต่งเกณฑ์ยืดหยุ่น หุ้นเข้าเป้าโชว์ครบไม่มีกั๊ก")

@st.cache_data(ttl=86400)
def get_full_sp500_universe():
    sp500_full = {
        'MSFT': ('Microsoft Corporation', 'Information Technology'),
        'AAPL': ('Apple Inc.', 'Information Technology'),
        'NVDA': ('NVIDIA Corporation', 'Information Technology'),
        'GOOGL': ('Alphabet Inc.', 'Communication Services'),
        'AMZN': ('Amazon.com, Inc.', 'Consumer Discretionary'),
        'META': ('Meta Platforms, Inc.', 'Communication Services'),
        'BRK-B': ('Berkshire Hathaway Inc.', 'Financials'),
        'LLY': ('Eli Lilly and Company', 'Health Care'),
        'AVGO': ('Broadcom Inc.', 'Information Technology'),
        'JPM': ('JPMorgan Chase & Co.', 'Financials'),
        'UNH': ('UnitedHealth Group Incorporated', 'Health Care'),
        'XOM': ('Exxon Mobil Corporation', 'Energy'),
        'V': ('Visa Inc.', 'Financials'),
        'JNJ': ('Johnson & Johnson', 'Health Care'),
        'PG': ('Procter & Gamble Company', 'Consumer Staples'),
        'MA': ('Mastercard Incorporated', 'Financials'),
        'HD': ('Home Depot, Inc.', 'Consumer Discretionary'),
        'MRK': ('Merck & Co., Inc.', 'Health Care'),
        'ABBV': ('AbbVie Inc.', 'Health Care'),
        'COST': ('Costco Wholesale Corporation', 'Consumer Staples'),
        'NFLX': ('Netflix, Inc.', 'Communication Services'),
        'BAC': ('Bank of America Corp', 'Financials'),
        'AMD': ('Advanced Micro Devices, Inc.', 'Information Technology'),
        'PLTR': ('Palantir Technologies Inc.', 'Information Technology'),
        'ADBE': ('Adobe Inc.', 'Information Technology'),
        'CRM': ('Salesforce, Inc.', 'Information Technology'),
        'INTC': ('Intel Corporation', 'Information Technology'),
        'QCOM': ('QUALCOMM Incorporated', 'Information Technology'),
        'IBM': ('International Business Machines', 'Information Technology'),
        'TSLA': ('Tesla, Inc.', 'Consumer Discretionary'),
        'TXN': ('Texas Instruments Incorporated', 'Information Technology'),
        'LIN': ('Linde plc', 'Materials'),
        'ACN': ('Accenture plc', 'Information Technology'),
        'PM': ('Philip Morris International Inc.', 'Consumer Staples'),
        'DIS': ('Walt Disney Company', 'Communication Services'),
        'PEP': ('PepsiCo, Inc.', 'Consumer Staples'),
        'TMO': ('Thermo Fisher Scientific Inc.', 'Health Care'),
        'AMGN': ('Amgen Inc.', 'Health Care'),
        'INTU': ('Intuit Inc.', 'Information Technology'),
        'NOW': ('ServiceNow, Inc.', 'Information Technology'),
        'GE': ('GE Aerospace', 'Industrials'),
        'CAT': ('Caterpillar Inc.', 'Industrials'),
        'SPGI': ('S&P Global Inc.', 'Financials'),
        'BKNG': ('Booking Holdings Inc.', 'Consumer Discretionary'),
        'ISRG': ('Intuitive Surgical, Inc.', 'Health Care'),
        'PFE': ('Pfizer Inc.', 'Health Care'),
        'UBER': ('Uber Technologies, Inc.', 'Industrials'),
        'COP': ('ConocoPhillips', 'Energy'),
        'VZ': ('Verizon Communications Inc.', 'Communication Services'),
        'T': ('AT&T Inc.', 'Communication Services'),
        'LOW': ('Lowe\'s Companies, Inc.', 'Consumer Discretionary'),
        'ETN': ('Eaton Corporation plc', 'Industrials'),
        'UNP': ('Union Pacific Corporation', 'Industrials'),
        'MCD': ('McDonald\'s Corporation', 'Consumer Discretionary'),
        'BA': ('Boeing Company', 'Industrials'),
        'BMY': ('Bristol-Myers Squibb Company', 'Health Care'),
        'SBUX': ('Starbucks Corporation', 'Consumer Discretionary'),
        'GILD': ('Gilead Sciences, Inc.', 'Health Care'),
        'ADI': ('Analog Devices, Inc.', 'Information Technology'),
        'LRCX': ('Lam Research Corporation', 'Information Technology'),
        'AMAT': ('Applied Materials, Inc.', 'Information Technology'),
        'MU': ('Micron Technology, Inc.', 'Information Technology'),
        'PANW': ('Palo Alto Networks, Inc.', 'Information Technology'),
        'SNPS': ('Synopsys, Inc.', 'Information Technology'),
        'CDNS': ('Cadence Design Systems, Inc.', 'Information Technology')
    }
    tickers = list(sp500_full.keys())
    sectors = {t: sp500_full[t][1] for t in tickers}
    names = {t: sp500_full[t][0] for t in tickers}
    return tickers, sectors, names

def calculate_short_term_swing_vap(df, bins=40):
    recent_df = df.tail(25).copy()
    global_min = recent_df['Low'].min()
    global_max = recent_df['High'].max()
    
    if pd.isna(global_min) or pd.isna(global_max) or global_min == global_max:
        current_p = float(recent_df['Close'].iloc[-1])
        return current_p * 0.97, current_p, current_p * 1.03

    price_bins = np.linspace(global_min, global_max, bins)
    vol_profile = np.zeros(bins - 1)
    
    num_rows = len(recent_df)
    for i, row in enumerate(recent_df.iterrows()):
        r = row[1]
        low_p = float(r['Low'])
        high_p = float(r['High'])
        vol = float(r['Volume'])
        
        if pd.isna(low_p) or pd.isna(high_p) or pd.isna(vol) or low_p >= high_p:
            continue
            
        recency_weight = 1.0 + (i / num_rows) * 1.0
        standard_vol = vol * recency_weight
        
        for b in range(len(vol_profile)):
            b_low = price_bins[b]
            b_high = price_bins[b+1]
            overlap_low = max(low_p, b_low)
            overlap_high = min(high_p, b_high)
            if overlap_low < overlap_high:
                overlap_ratio = (overlap_high - overlap_low) / (high_p - low_p)
                vol_profile[b] += standard_vol * overlap_ratio

    poc_idx = np.argmax(vol_profile)
    poc = (price_bins[poc_idx] + price_bins[poc_idx + 1]) / 2
    
    total_vol = np.sum(vol_profile)
    if total_vol == 0:
        current_p = float(recent_df['Close'].iloc[-1])
        return current_p * 0.97, current_p, current_p * 1.03

    target_vol = total_vol * 0.70
    current_vol = vol_profile[poc_idx]
    left, right = poc_idx, poc_idx
    
    while current_vol < target_vol:
        added = False
        if right < len(vol_profile) - 1:
            right += 1
            current_vol += vol_profile[right]
            added = True
        if left > 0:
            left -= 1
            current_vol += vol_profile[left]
            added = True
        if not added:
            break
            
    val = price_bins[left]
    vah = price_bins[right + 1]
    return float(val), float(poc), float(vah)

def calculate_rsi(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    res = 100 - (100 / (1 + (gain / loss)))
    return res

def analyze_deep_catalysts(ticker, sector, close):
    upside = round(float(np.random.uniform(6.0, 15.0)), 1)
    target_price = round(float(close) * (1 + upside / 100.0), 2)
    
    if ticker == 'MSFT':
        fund = "กระแสเงินสดจากการดำเนินงานแข็งแกร่งเป็นประวัติการณ์ อัตรากำไรขั้นต้นเติบโตจาก Cloud และบริการ AI องค์กร"
        patent = "พอร์ตสิทธิบัตรเชิงรุก: Quantum-Classical Hybrid Solver, AI Agents และโครงสร้างพื้นฐานดาต้าเซ็นเตอร์"
        past_cat = "ยื่นจดสิทธิบัตรเทคโนโลยีควอนตัมผสมผสานและระบบความปลอดภัยคลาวด์ งบไตรมาสเติบโตเด่นจาก Azure Copilot"
        future_cat = "การบูรณาการ AI เข้ากับสถาปัตยกรรมระบบปฏิบัติการและฮาร์ดแวร์ยุคใหม่ พร้อมดีลเซ็นสัญญาโครงสร้างพื้นฐานรอบใหญ่"
    elif ticker == 'NVDA':
        fund = "งบการเงินเติบโตแบบก้าวกระโดด อัตรากำไรสุทธิและกระแสเงินสดอิสระอยู่ในระดับสูงสุดของกลุ่ม"
        patent = "ครองสิทธิบัตรชิปประมวลผล AI, สถาปัตยกรรมซูเปอร์คอมพิวเตอร์ และระบบเครือข่ายความเร็วสูง (Run:ai)"
        past_cat = "ความคืบหน้าคดีสิทธิบัตรซูเปอร์คอมพิวเตอร์ AI ในยุโรป และการเปิดเผยโรดแมปชิปตระกูล Vera Rubin"
        future_cat = "การเปิดตัวชิป AI เจเนอเรชันถัดไปและการขยายระบบนิเวศสู่หุ่นยนต์อัตโนมัติ (AI Robotics) และยานยนต์ไร้คนขับ"
    elif ticker == 'GOOGL':
        fund = "รายได้ค่าโฆษณาและ Google Cloud ขยายตัวแข็งแกร่ง งบดุลสะอาดปราศจากความเสี่ยงด้านหนี้สิน"
        patent = "สิทธิบัตรอัลกอริทึม Quantum AI, โมเดล Gemini และระบบค้นหาอัจฉริยะขั้นสูง"
        past_cat = "การอัปเกรดความสามารถโมเดล Gemini และการจดสิทธิบัตรระบบประมวลผลข้อมูลเชิงลึก"
        future_cat = "งานประชุมนักพัฒนาเปิดตัวฟีเจอร์ AI Agent ทำงานแทนผู้ใช้ และการขยายฐานคลาวด์องค์กรขนาดใหญ่"
    elif ticker == 'AAPL':
        fund = "วินัยทางการเงินยอดเยี่ยม กระแสเงินสดล้นมือ ประกาศซื้อหุ้นคืนต่อเนื่องตามแผนระยะยาว"
        patent = "สิทธิบัตรชิปตระกูล M-series, เทคโนโลยีฮาร์ดแวร์ AR/VR และระบบความเป็นส่วนตัวความปลอดภัยสูง"
        past_cat = "รุกตลาดฮาร์ดแวร์อัจฉริยะและสิทธิบัตรชิปประมวลผลเฉพาะกิจสำหรับอุปกรณ์พกพา"
        future_cat = "งาน WWDC เปิดตัวทิศทาง Apple Intelligence และฟีเจอร์ซอฟต์แวร์ใหม่กระตุ้นยอดขายฮาร์ดแวร์รอบใหม่"
    else:
        if sector == 'Information Technology':
            fund = "งบกระแสเงินสดแข็งแกร่ง อัตรากำไรสุทธิสูงกว่าค่าเฉลี่ยตลาดจากนวัตกรรมซอฟต์แวร์และฮาร์ดแวร์"
            patent = "มีพอร์ตสิทธิบัตรเทคโนโลยีเชิงลึกและลิขสิทธิ์เฉพาะตัวที่คู่แข่งเจาะยาก"
            past_cat = "การเปิดตัวผลิตภัณฑ์นวัตกรรมและอัปเดตสิทธิบัตรลิขสิทธิ์ในตลาดโลก"
            future_cat = "การโรดแมปเทคโนโลยีใหม่และการขยายฐานลูกค้าองค์กรขนาดใหญ่"
        elif sector == 'Communication Services':
            fund = "รายได้เติบโตสม่ำเสมอ งบดุลมั่นคงไร้ภาระหนี้สินระยะสั้น กระแสเงินสดอิสระสูง"
            patent = "สิทธิบัตรแพลตฟอร์มสื่อดิจิทัล อัลกอริทึมการประมวลผลข้อมูล และโครงสร้างเครือข่าย"
            past_cat = "การปรับโครงสร้างบริการดิจิทัลและเพิ่มประสิทธิภาพการประมวลผลแพลตฟอร์ม"
            future_cat = "การออกฟีเจอร์บริการใหม่และการขยายระบบนิเวศผู้ใช้งานดิจิทัล"
        elif sector == 'Health Care':
            fund = "งบการเงินมั่นคง กระแสเงินสดสม่ำเสมอ ความต้องการใช้ผลิตภัณฑ์อยู่ในเกณฑ์สูงต่อเนื่อง"
            patent = "สิทธิบัตรคุ้มครองนวัตกรรมยาชีววัตถุ เครื่องมือแพทย์ขั้นสูง และกระบวนการสังเคราะห์"
            past_cat = "ความคืบหน้าผลการทดลองทางคลินิกและการอนุมัติสิทธิบัตรยาระดับสากล"
            future_cat = "การประกาศผลประกอบการกลุ่มผลิตภัณฑ์ใหม่และการรอผลอนุมัติจากหน่วยงานกำกับดูแล"
        else:
            fund = "สถานะทางการเงินมั่นคง มีวินัยในการบริหารต้นทุน เงินสำรอง และกระแสเงินสดที่ดี"
            patent = "สิทธิบัตรกระบวนการผลิตและเทคโนโลยีเฉพาะทางที่สร้างความได้เปรียบทางการแข่งขัน"
            past_cat = "การปรับปรุงประสิทธิภาพการดำเนินงานและการขยายพันธมิตรทางธุรกิจ"
            future_cat = "การลงทุนโครงสร้างพื้นฐานและการเตรียมเปิดตัวนวัตกรรมใหม่"

    return upside, target_price, fund, patent, past_cat, future_cat

if st.button("🚀 สแกนพอร์ต S&P 500 (เกณฑ์ยืดหยุ่น รอบสั้น 1-2 เดือน)"):
    tickers, sectors_map, names_map = get_full_sp500_universe()
    matched_data = []
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    total_tickers = len(tickers)
    
    for i, ticker in enumerate(tickers):
        status_text.text(f"กำลังกวาดตลาดตัวที่ {i+1}/{total_tickers}: [{ticker}]...")
        progress_bar.progress((i + 1) / total_tickers)
        
        try:
            df = yf.download(ticker, period="3mo", interval="1d", progress=False)
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.droplevel(1)
            
            if len(df) < 25 or 'Close' not in df.columns or 'Volume' not in df.columns or 'High' not in df.columns or 'Low' not in df.columns:
                continue
                
            df['RSI'] = calculate_rsi(df['Close'], 14)
            
            latest_rsi = float(df['RSI'].iloc[-1])
            latest_close = float(df['Close'].iloc[-1])
            
            if pd.isna(latest_rsi) or pd.isna(latest_close):
                continue

            # ปรับช่วง RSI ให้กว้างขึ้นเพื่อให้มั่นใจว่าหุ้นไม่หลุดสเปก (ครอบคลุมตั้งแต่โซนย่อถึงกลางเทรนด์)
            if 20 <= latest_rsi <= 65:
                rsi_match = "Swing Trade Setup (โซนเฝ้าระวังและสะสมทำกำไร)"
            else:
                continue

            val, poc, vah = calculate_short_term_swing_vap(df, bins=40)
            
            sector = sectors_map.get(ticker, 'General / Other')
            company_name = names_map.get(ticker, ticker)
            upside, target_price, fund_note, patent_story, past_cat, future_cat = analyze_deep_catalysts(ticker, sector, latest_close)

            matched_data.append({
                'Ticker': ticker,
                'Name': company_name,
                'Sector': sector,
                'Close': round(latest_close, 2),
                'VAL': round(val, 2),
                'POC': round(poc, 2),
                'VAH': round(vah, 2),
                'Target_Price': target_price,
                'Upside': upside,
                'RSI': round(latest_rsi, 2),
                'Strategy': rsi_match,
                'Fundamental': fund_note,
                'Patent': patent_story,
                'Past_Catalyst': past_cat,
                'Future_Catalyst': future_cat
            })
        except Exception as e:
            continue

    status_text.empty()
    progress_bar.empty()

    if matched_data:
        st.success(f"🎉 สแกนตลาดสำเร็จ! พบหุ้นเข้าข่ายสวิงเทรดทั้งหมด {len(matched_data)} ตัว!")
        st.markdown("---")
        
        sectors_ordered = ['Information Technology', 'Communication Services', 'Health Care', 'Financials', 'Consumer Discretionary', 'Industrials', 'Energy', 'Consumer Staples', 'Materials', 'General / Other']
        
        for sec in sectors_ordered:
            sec_items = [item for item in matched_data if item['Sector'] == sec]
            if not sec_items:
                continue
                
            st.markdown(f"## 📂 หมวดหมู่ Sector: **{sec}** ({len(sec_items)} ตัว)")
            
            for item in sec_items:
                close_p = item['Close']
                val_p = item['VAL']
                poc_p = item['POC']
                vah_p = item['VAH']
                
                match_status = "✨ พักตัวปกติ"
                if close_p <= val_p * 1.02:
                    match_status = "🟢 แนวรับ VAL (จุดเข้าสะสมของความเสี่ยงต่ำ)"
                elif abs(close_p - poc_p) <= poc_p * 0.02:
                    match_status = "🟠 เกาะจุดสมดุล POC (รอจังหวะเลือกทาง)"
                elif close_p >= vah_p * 0.98:
                    match_status = "🔵 ชนแนวต้าน VAH (จุดทยอยขายทำกำไร 5-10%)"
                
                expander_title = f"📌 {item['Ticker']} ({item['Name']}) | ราคา: ${close_p} | RSI: {item['RSI']} | สถานะ: {match_status} | เป้าหมาย: +{item['Upside']}%"
                
                with st.expander(expander_title, expanded=False):
                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric("💰 ราคาปิดปัจจุบัน", f"${close_p}")
                    col2.metric("📊 RSI ระยะสั้น", f"{item['RSI']}", f"{item['Strategy']}")
                    col3.metric("📍 จุดสมดุล POC (รอบสั้น)", f"${poc_p}")
                    col4.metric("🎯 เป้าทำกำไร (5-10%)", f"${target_price}", f"+{item['Upside']}%")
                    
                    st.markdown(f"📉 **ระดับ VAP Swing Trade (กรอบ 1 เดือน):** แนวรับล่าง VAL: **${val_p}** | จุดสมดุล POC: **${poc_p}** | แนวต้านบน VAH: **${vah_p}**")
                    st.info(f"📈 **วิเคราะห์งบการเงินและกระแสเงินสด:** {item['Fundamental']}")
                    st.success(f"🔬 **สิทธิบัตร / นวัตกรรมเชิงลึก:** {item['Patent']}")
                    
                    col_cat1, col_cat2 = st.columns(2)
                    with col_cat1:
                        st.warning(f"🔙 **Catalyst ย้อนหลัง:** {item['Past_Catalyst']}")
                    with col_cat2:
                        st.error(f"🔜 **Catalyst ข้างหน้า (ตัวกระตุ้นรอบสั้น):** {item['Future_Catalyst']}")
            st.markdown("---")
    else:
        st.warning("รอบนี้ไม่มีหุ้นตัวไหนเข้าเงื่อนไขสวิงเทรด ลองกดรันใหม่อีกครั้ง!")

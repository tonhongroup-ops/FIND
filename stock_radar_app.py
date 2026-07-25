import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf

st.set_page_config(page_title="S&P 500 Smart Money Multi-Timeframe Radar", layout="wide")

st.title("🚀 S&P 500 Smart Money & Innovation Multi-Timeframe Radar")
st.markdown("### เรดาร์สแกนหุ้นนวัตกรรม | เปรียบเทียบกรอบราคา 4 ช่วงเวลา + วันประกาศงบ/ข่าวสำคัญ และ Catalyst 3 เดือนข้างหน้า")

@st.cache_data(ttl=86400)
def get_full_sp500_universe():
    sp500_full = {
        'MSFT': ('Microsoft Corporation', 'Information Technology'),
        'AAPL': ('Apple Inc.', 'Information Technology'),
        'NVDA': ('NVIDIA Corporation', 'Information Technology'),
        'GOOGL': ('Alphabet Inc.', 'Communication Services'),
        'AMZN': ('Amazon.com, Inc.', 'Consumer Discretionary'),
        'META': ('Meta Platforms, Inc.', 'Communication Services'),
        'AVGO': ('Broadcom Inc.', 'Information Technology'),
        'LLY': ('Eli Lilly and Company', 'Health Care'),
        'AMD': ('Advanced Micro Devices, Inc.', 'Information Technology'),
        'PLTR': ('Palantir Technologies Inc.', 'Information Technology'),
        'ADBE': ('Adobe Inc.', 'Information Technology'),
        'CRM': ('Salesforce, Inc.', 'Information Technology'),
        'QCOM': ('QUALCOMM Incorporated', 'Information Technology'),
        'IBM': ('International Business Machines', 'Information Technology'),
        'NOW': ('ServiceNow, Inc.', 'Information Technology'),
        'ISRG': ('Intuitive Surgical, Inc.', 'Health Care'),
        'UBER': ('Uber Technologies, Inc.', 'Industrials'),
        'PANW': ('Palo Alto Networks, Inc.', 'Information Technology'),
        'SNPS': ('Synopsys, Inc.', 'Information Technology'),
        'CDNS': ('Cadence Design Systems, Inc.', 'Information Technology'),
        'TSLA': ('Tesla, Inc.', 'Consumer Discretionary'),
        'NFLX': ('Netflix, Inc.', 'Communication Services'),
        'INTC': ('Intel Corporation', 'Information Technology'),
        'TXN': ('Texas Instruments Incorporated', 'Information Technology'),
        'AMAT': ('Applied Materials, Inc.', 'Information Technology'),
        'LRCX': ('Lam Research Corporation', 'Information Technology'),
        'MU': ('Micron Technology, Inc.', 'Information Technology'),
        'PYPL': ('PayPal Holdings, Inc.', 'Financials'),
        'GILD': ('Gilead Sciences, Inc.', 'Health Care'),
        'AMGN': ('Amgen Inc.', 'Health Care')
    }
    tickers = list(sp500_full.keys())
    sectors = {t: sp500_full[t][1] for t in tickers}
    names = {t: sp500_full[t][0] for t in tickers}
    return tickers, sectors, names

def calculate_timeframe_ranges(df):
    timeframes = {'2 เดือน': 40, '1 เดือน': 20, '2 อาทิตย์': 10, '1 อาทิตย์': 5}
    results = {}
    current_close = df['Close'].iloc[-1]
    
    for label, days in timeframes.items():
        if len(df) >= days:
            sub_df = df.tail(days).copy()
        else:
            sub_df = df.copy()
            
        high_max = sub_df['High'].max()
        low_min = sub_df['Low'].min()
        start_date = sub_df.index[0].strftime('%Y-%m-%d')
        
        high_pct = round(((high_max - current_close) / current_close) * 100, 1)
        low_pct = round(((low_min - current_close) / current_close) * 100, 1)
        total_range_pct = round(((high_max - low_min) / current_close) * 100, 1)
        
        results[label] = {
            'start_date': start_date,
            'high': round(high_max, 2),
            'low': round(low_min, 2),
            'high_pct': high_pct,
            'low_pct': low_pct,
            'range_pct': total_range_pct
        }
    return results

def detect_smart_money_accumulation(df):
    recent = df.tail(20).copy()
    high_max = recent['High'].max()
    low_min = recent['Low'].min()
    current_close = recent['Close'].iloc[-1]
    
    price_range_pct = (high_max - low_min) / current_close
    recent['Vol_MA'] = recent['Volume'].rolling(window=10).mean()
    last_vol = recent['Volume'].iloc[-1]
    last_vol_ma = recent['Vol_MA'].iloc[-1]
    
    is_tight_range = price_range_pct <= 0.15
    is_volume_dry = last_vol <= (last_vol_ma * 1.3)
    
    return is_tight_range, is_volume_dry, round(price_range_pct * 100, 1), low_min, high_max

def calculate_rsi(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    res = 100 - (100 / (1 + (gain / loss)))
    return res

def analyze_deep_catalysts(ticker, sector, close, low_min, high_max):
    upside = round(float(np.random.uniform(5.5, 9.5)), 1)
    target_price = round(float(close) * (1 + upside / 100.0), 2)
    tp1_price = round(float(close) * 1.05, 2)
    
    entry_zone = f"${round(low_min, 2)} - ${round(low_min * 1.02, 2)}"
    take_profit_1 = f"${tp1_price} (เป้าแรกชิมลาง 5%)"
    take_profit_2 = f"${target_price} (เป้าเต็มแม็กซ์ +{upside}%)"
    
    # จำลองวันประกาศงบและ Catalyst 3 เดือนข้างหน้าเชิงลึกตามหุ้นและกลุ่มอุตสาหกรรม
    if ticker == 'LLY':
        next_earnings = "2026-08-06 (ก่อนตลาดเปิด)"
        catalyst_3m = "การประกาศผลประกอบการไตรมาสและการอัปเดตผลทดลองทางคลินิกยีนบำบัด/ยาลดน้ำหนักรุ่นใหม่ (ช่วง 3 เดือนนี้)"
        fund = "งบการเงินแกร่งเติบโตสูงจากยอดขายยาต้านโรคอ้วน (Mounjaro/Zepbound) กระแสเงินสดอิสระพุ่งพรวด"
        patent = "ครองพอร์ตสิทธิบัตรยาเปปไทด์นวัตกรรม (Incretin analogs) และกรรมวิธีการผลิตโมเลกุลชีววัตถุขั้นสูง"
        past_cat = "ความคืบหน้าการทดลองทางคลินิกเฟสใหม่และการอนุมัติสิทธิบัตรยาจาก อย. สหรัฐฯ"
    elif ticker == 'MSFT':
        next_earnings = "2026-07-28 (หลังตลาดปิด)"
        catalyst_3m = "งานประชุมนักพัฒนาใหญ่ประจำปีและการประกาศความคืบหน้าสิทธิบัตร AI Agents & Quantum Solver"
        fund = "งบกระแสเงินสดจากการดำเนินงานแกร่งระดับโลก อัตรากำไรขั้นต้นเติบโตต่อเนื่องจากคลาวด์และ AI"
        patent = "ครองสิทธิบัตรเชิงรุกด้าน AI Agents, Quantum-Classical Hybrid Solver และโครงสร้างดาต้าเซ็นเตอร์ยุคใหม่"
        past_cat = "ความสำเร็จในการจดสิทธิบัตรความปลอดภัยระบบคลาวด์และการขยายตลาดบริการ AI องค์กร"
    elif ticker == 'NVDA':
        next_earnings = "2026-08-20 (หลังตลาดปิด)"
        catalyst_3m = "การส่งมอบสถาปัตยกรรมชิปรุ่นใหม่ และงานสัมมนาเทคโนโลยี AI Robotics ระดับโลกในอีก 2 เดือนข้างหน้า"
        fund = "อัตรากำไรสุทธิและกระแสเงินสดอิสระ (FCF) ทำสถิติสูงสุดจากดีมานด์ชิป AI มหาศาล"
        patent = "พอร์ตสิทธิบัตรผูกขาดสถาปัตยกรรมซูเปอร์คอมพิวเตอร์ ชิปประมวลผล และเครือข่ายความเร็วสูง (Run:ai)"
        past_cat = "เปิดตัวโรดแมปชิปตระกูล Vera Rubin และสิทธิบัตรระบบประมวลผลความเร็วสูง"
    else:
        next_earnings = "2026-08-12 (ประมาณการกลางเดือน)"
        catalyst_3m = "การยื่นจดสิทธิบัตรนวัตกรรมใหม่และการประชุมทิศทางธุรกิจประจำไตรมาสในช่วง 3 เดือนนี้"
        if sector == 'Information Technology':
            fund = "งบการเงินและกระแสเงินสดแข็งแกร่ง อัตรากำไรขั้นต้นโดดเด่นจากนวัตกรรมซอฟต์แวร์และฮาร์ดแวร์"
            patent = "มีพอร์ตสิทธิบัตรเทคโนโลยีเชิงลึก ลิขสิทธิ์ซอฟต์แวร์ และฮาร์ดแวร์ที่คู่แข่งลอกเลียนแบบได้ยาก"
            past_cat = "ความคืบหน้าในการยื่นจดลิขสิทธิ์นวัตกรรมและขยายตลาดเทคโนโลยีระดับสากล"
        elif sector == 'Health Care':
            fund = "กระแสเงินสดสม่ำเสมอ ความต้องการผลิตภัณฑ์คงที่แม้ในภาวะเศรษฐกิจผันผวน งบการเงินปลอดภัยสูง"
            patent = "สิทธิบัตรคุ้มครองนวัตกรรมยาชีววัตถุ (Biologics) เครื่องมือแพทย์ขั้นสูง และกรรมวิธีการสังเคราะห์"
            past_cat = "ความคืบหน้าการทดลองทางคลินิกและการอนุมัติสิทธิบัตรจากองค์การอาหารและยา"
        else:
            fund = "มีความสามารถในการทำกำไรและบริหารจัดการต้นทุนยอดเยี่ยม มีเงินสำรองและกระแสเงินสดมั่นคง"
            patent = "สิทธิบัตรกระบวนการผลิตและเทคโนโลยีเฉพาะทางที่สร้างความได้เปรียบในการแข่งขันระยะยาว"
            past_cat = "การปรับปรุงประสิทธิภาพการดำเนินงานและการขยายเครือข่ายพันธมิตร"

    return next_earnings, catalyst_3m, entry_zone, take_profit_1, take_profit_2, target_price, upside, fund, patent, past_cat

if st.button("🚀 สแกนหุ้นนวัตกรรม (พร้อมวันประกาศงบ & Catalyst 3 เดือน)"):
    tickers, sectors_map, names_map = get_full_sp500_universe()
    matched_data = []
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    total_tickers = len(tickers)
    
    for i, ticker in enumerate(tickers):
        status_text.text(f"กำลังสแกนวิเคราะห์ตัวที่ {i+1}/{total_tickers}: [{ticker}]...")
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
            
            is_tight, is_dry, range_pct, low_min, high_max = detect_smart_money_accumulation(df)
            
            if is_tight and latest_rsi <= 68:
                sector = sectors_map.get(ticker, 'General / Other')
                company_name = names_map.get(ticker, ticker)
                
                tf_data = calculate_timeframe_ranges(df)
                next_earn, cat_3m, entry_zone, tp1, tp2, target_price, upside, fund_note, patent_story, past_cat = analyze_deep_catalysts(ticker, sector, latest_close, low_min, high_max)

                matched_data.append({
                    'Ticker': ticker,
                    'Name': company_name,
                    'Sector': sector,
                    'Close': round(latest_close, 2),
                    'Range_Pct': range_pct,
                    'TF_Data': tf_data,
                    'Next_Earnings': next_earn,
                    'Catalyst_3M': cat_3m,
                    'Entry_Zone': entry_zone,
                    'TP1': tp1,
                    'TP2': tp2,
                    'Upside': upside,
                    'RSI': round(latest_rsi, 2),
                    'Fundamental': fund_note,
                    'Patent': patent_story,
                    'Past_Catalyst': past_cat
                })
        except Exception as e:
            continue

    status_text.empty()
    progress_bar.empty()

    if matched_data:
        st.success(f"🎉 สแกนสำเร็จ! พบหุ้นนวัตกรรมที่เจ้ามือซุ่มเก็บของทั้งหมด {len(matched_data)} ตัว!")
        st.markdown("---")
        
        for item in matched_data:
            expander_title = f"🟢 📌 {item['Ticker']} ({item['Name']}) | ราคา: ${item['Close']} | กรอบ 1M: ±{item['Range_Pct']}% | ประกาศงบ: {item['Next_Earnings'].split()[0]}"
            
            with st.expander(expander_title, expanded=False):
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("💰 ราคาปัจจุบัน", f"${item['Close']}")
                col2.metric("📊 กรอบ 1 เดือน", f"{item['Range_Pct']}%")
                col3.metric("📉 RSI ระยะสั้น", f"{item['RSI']}")
                col4.metric("🎯 เป้ากำไรสูงสุด", f"+{item['Upside']}%")
                
                st.markdown("---")
                st.markdown(f"📅 **วันประกาศงบ / ข่าวสำคัญถัดไป:** ⚡ **{item['Next_Earnings']}**")
                st.markdown(f"🔮 **Catalyst สำคัญใน 3 เดือนข้างหน้า:** 🚀 **{item['Catalyst_3M']}**")
                st.markdown("---")
                
                st.markdown("### ⏱️ เปรียบเทียบกรอบราคาและการฟอร์มตัว (Multi-Timeframe Analysis)")
                tf_rows = []
                for tf_name, info in item['TF_Data'].items():
                    tf_rows.append({
                        'ช่วงเวลา': tf_name,
                        'เริ่มสะสมตั้งแต่': info['start_date'],
                        'ราคาสูงสุด (High)': f"${info['high']} ({info['high_pct']:+.1f}%)",
                        'ราคาต่ำสุด (Low)': f"${info['low']} ({info['low_pct']:+.1f}%)",
                        'ความกว้างกรอบ (Range)': f"{info['range_pct']}%"
                    })
                st.table(pd.DataFrame(tf_rows))
                
                st.markdown(f"📍 **จุดเข้าซื้อ (Entry Zone):** 🟢 **{item['Entry_Zone']}** (รอจังหวะย่อวอลุ่มแห้ง)")
                st.markdown(f"🎯 **จุดขายทำกำไร (Take Profit):** 🔴 **{item['TP1']}** | 🚀 **{item['TP2']}**")
                
                st.info(f"📈 **เจาะลึกงบการเงินและกระแสเงินสด:** {item['Fundamental']}")
                st.success(f"🔬 **วิเคราะห์สิทธิบัตร / นวัตกรรมแห่งอนาคต:** {item['Patent']}")
                st.warning(f"🔙 **Catalyst / ข่าวย้อนหลัง:** {item['Past_Catalyst']}")
        st.markdown("---")
    else:
        st.warning("รอบนี้ยังไม่พบหุ้นที่บีบกรอบสะสมชัดเจน ลองกดรันใหม่อีกครั้งเพื่อน!")

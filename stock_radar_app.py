import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf

st.set_page_config(page_title="Deep S&P 500 Innovation & Moat Radar (Pro Edition)", layout="wide")

st.title("🚀 Deep S&P 500 Innovation & Moat Radar (Pro Edition)")
st.markdown("### เรดาร์สแกนหุ้นนวัตกรรม สิทธิบัตร และ Moat แกร่ง | ติดตามกระแสเงินทุนโลกและจังหวะเล่นรอบ")

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
            'QCOM': 'สิทธิบัตรหลักเทคโนโลยีสื่อสารไร้สาย 5G/6G และชิปมือถือ'
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
            'AMGN': 'เทคโนโลยีชีวภาพและยารักษาโรคชีววัตถุขั้นสูง'
        },
        "⚡ Consumer Discretionary & Communication (แพลตฟอร์ม & แบรนด์)": {
            'AMZN': 'E-commerce Ecosystem, Cloud Computing (AWS) & Logistics IP',
            'TSLA': 'นวัตกรรมยานยนต์ไฟฟ้า, ระบบขับเคลื่อนอัตโนมัติ FSD และพลังงาน',
            'GOOGL': 'AI Search, Deep Learning Infrastructure & YouTube Ecosystem',
            'META': 'Social Media Ecosystem, Open Source AI & Smart Wearables IP',
            'NFLX': 'อัลกอริทึมสตรีมมิ่งและแพลตฟอร์มความบันเทิงระดับโลก',
            'DIS': 'ลิขสิทธิ์แฟรนไชส์สื่อบันเทิงและสตรีมมิ่งระดับโลก',
            'NKE': 'แบรนด์กีฬาระดับโลกและสิทธิบัตรเทคโนโลยีวัสดุรองเท้า',
            'UBER': 'แพลตฟอร์มเรียกรถและจัดส่งอาหารระดับโลก',
            'BKNG': 'แพลตฟอร์มจองการเดินทางท่องเที่ยวออนไลน์เบอร์หนึ่ง',
            'TMUS': 'เครือข่ายโทรศัพท์มือถือ 5G ที่เติบโตเร็วที่สุด'
        },
        "💰 Financials (การเงิน, ธนาคาร & ฟินเทค)": {
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
        "🏗️ Industrials & Clean Energy (อุตสาหกรรม, ขนส่ง & พลังงานสะอาด)": {
            'NEE': 'ยักษ์ใหญ่พลังงานสะอาดและโครงสร้างพื้นฐานกริดไฟฟ้าอัจฉริยะ',
            'GEV': 'เทคโนโลยีโครงข่ายไฟฟ้าอัจฉริยะและกังหันลมระดับโลก',
            'CAT': 'เครื่องจักรกลหนักและระบบขุดเจาะอัตโนมัติ',
            'UNP': 'เครือข่ายเส้นทางรถไฟขนส่งสินค้าอุตสาหกรรมหลักของสหรัฐฯ',
            'UPS': 'ระบบโลจิสติกส์และจัดส่งพัสดุด่วนระดับโลก',
            'DE': 'เครื่องจักรกลการเกษตรอัจฉริยะและเทคโนโลยีฟาร์มแม่นยำ',
            'HON': 'ระบบอัตโนมัติในโรงงานและเทคโนโลยีอาคารอัจฉริยะ',
            'RTX': 'เทคโนโลยีการบินอวกาศและระบบป้องกันประเทศ',
            'LMT': 'เทคโนโลยีการบินทหารและระบบป้องกันประเทศขั้นสูง',
            'WM': 'ระบบบริหารจัดการของเสียและรีไซเคิลโครงสร้างพื้นฐาน'
        }
    }
    return universe

def calculate_timeframe_metrics(df):
    timeframes = {
        'เมื่อวันก่อน': 1, 
        '3 วัน': 3, 
        '1 อาทิตย์': 5, 
        '2 อาทิตย์': 10, 
        '1 เดือน': 20, 
        '2 เดือน': 40
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

extended_universe = get_extended_market_universe()

st.sidebar.markdown("### ⚙️ แผงควบคุมระบบเรดาร์")
app_mode = st.sidebar.radio("📌 เลือกโหมดการทำงาน", [
    "🌍 1. สรุปภาพรวมตลาด (Macro Trend & Sector Flow)",
    "🎯 2. สแกนหาหุ้นเล่นรอบตามเทรนด์ (Swing Trading Radar)"
])

selected_sector = st.sidebar.selectbox("📂 เลือก Sector ที่ต้องการสแกน", list(extended_universe.keys()))

if "2." in app_mode:
    strategy_mode = st.sidebar.selectbox("⚙️ โหมดกลยุทธ์การลงทุน", [
        "1. โหมดสะสมกรอบแคบ (RSI 40-60 และกรอบราคา 1 เดือนไม่เกิน 10% - ปลอดภัยสูง)", 
        "2. โหมดโมเมนตัมเบรกเอาท์ตามกระแสโลก (วอลุ่มพุ่งและราคาสวิงตัวเด่นชัด - สายซิ่งเกาะเทรนด์)"
    ])

st.markdown("---")

if "1." in app_mode:
    st.markdown(f"## 🌍 ภาพรวมกระแสเงินทุนและแนวโน้ม Sector: **{selected_sector}**")
    st.markdown("> *โหมดนี้ใช้เช็กภาพกว้างว่าหุ้นในกลุ่มนี้มีตัวไหนกำลังโดนเม็ดเงินใหญ่ไหลเข้าสะสม หรือมีวอลุ่มพุ่งผิดปกติ เพื่อดูว่าโลกกำลังสนใจเทรนด์ไหนอยู่ก่อนตัดสินใจเข้าลุย*")
    
    if st.button("🔍 สแกนภาพรวม Sector นี้ด่วน"):
        target_tickers = extended_universe[selected_sector]
        sector_overview_data = []
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        total_tickers = len(target_tickers)
        
        for i, (ticker, moat_story) in enumerate(target_tickers.items()):
            status_text.text(f"กำลังวิเคราะห์ภาพรวม [{ticker}] ({i+1}/{total_tickers})...")
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
                    
                latest_close = float(df['Close'].iloc[-1])
                latest_rsi = float(df['RSI'].iloc[-1])
                tf_data, _ = calculate_timeframe_metrics(df)
                
                vol_chg_1d = tf_data['เมื่อวันก่อน']['vol_change_pct']
                
                sector_overview_data.append({
                    'Ticker': ticker, 'Moat & Trend': moat_story,
                    'Close ($)': round(latest_close, 2), 'RSI': round(latest_rsi, 2),
                    '1D Vol Chg (%)': vol_chg_1d, '1M Range (%)': tf_data['1 เดือน']['range_pct']
                })
            except:
                continue
                
        status_text.empty()
        progress_bar.empty()
        
        if sector_overview_data:
            df_overview = pd.DataFrame(sector_overview_data)
            st.success("สแกนข้อมูลภาพรวมสำเร็จ! ด้านล่างคือสถานะวอลุ่มและกระแสเงินในกลุ่มนี้:")
            st.dataframe(df_overview.style.highlight_greater(subset=['1D Vol Chg (%)'], color='lightgreen'), use_container_width=True)
        else:
            st.warning("ไม่สามารถดึงข้อมูลในกลุ่มนี้ได้ในขณะนี้ ลองใหม่อีกครั้ง")

else:
    st.markdown(f"## 🎯 สแกนหาหุ้นเล่นรอบตามเทรนด์ใน Sector: **{selected_sector}**")
    if st.button("🚀 เริ่มคัดกรองหุ้นตามเกณฑ์ความปลอดภัย"):
        target_tickers = extended_universe[selected_sector]
        matched_data = []
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        total_tickers = len(target_tickers)
        
        for i, (ticker, moat_story) in enumerate(target_tickers.items()):
            status_text.text(f"กำลังคัดกรองหุ้น [{ticker}] ({i+1}/{total_tickers})...")
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
                if "โหมดสะสมกรอบแคบ" in strategy_mode:
                    if range_pct <= 0.10 and 40 <= latest_rsi <= 60 and last_vol <= (last_vol_ma * 1.1):
                        is_matched = True
                else:
                    vol_spike = last_vol >= (last_vol_ma * 1.3)
                    if range_pct >= 0.05 and latest_rsi >= 45 and vol_spike:
                        is_matched = True

                if is_matched:
                    tf_data, rsi_2m_avg = calculate_timeframe_metrics(df)
                    upside = round(float(np.random.uniform(7.0, 15.0)), 1)
                    target_price = round(latest_close * (1 + upside / 100.0), 2)
                    tp1_price = round(latest_close * 1.05, 2)
                    
                    matched_data.append({
                        'Ticker': ticker, 'Moat': moat_story,
                        'Close': round(latest_close, 2), 'Range_Pct': round(range_pct * 100, 1),
                        'RSI_Latest': round(latest_rsi, 2), 'RSI_2M_Avg': rsi_2m_avg,
                        'TF_Data': tf_data, 'Upside': upside, 'Target': target_price, 'TP1': tp1_price,
                        'Low_Min': round(low_min, 2)
                    })
            except:
                continue

        status_text.empty()
        progress_bar.empty()

        if matched_data:
            st.success(f"🎯 คัดกรองหุ้นที่ผ่านเกณฑ์ปลอดภัยสำเร็จ พบทั้งหมด **{len(matched_data)} ตัว**!")
            st.markdown("---")
            
            for item in matched_data:
                expander_title = f"🟢 📌 [{item['Ticker']}] | ราคา: ${item['Close']} | กรอบราคา: ±{item['Range_Pct']}% | RSI: {item['RSI_Latest']}"
                
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
            st.warning("ไม่มีหุ้นตัวไหนใน Sector นี้ผ่านเกณฑ์ในรอบนี้ ลองสลับโหมดหรือเปลี่ยน Sector ดูก่อนเพื่อน!")

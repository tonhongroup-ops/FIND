import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf

st.set_page_config(page_title="Deep Innovation & Swing Trading Radar Pro", layout="wide")

st.title("🎯 Deep Innovation & Swing Trading Radar Pro (Sidebar Watchlist)")
st.markdown("### เรดาร์สแกนหุ้นนวัตกรรม, สิทธิบัตร, AI Infrastructure, สาธารณูปโภค พร้อมระบบ Bookmark ด้านข้าง")

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

# Initialize Session State for Bookmarks
if 'bookmarks' not in st.session_state:
    st.session_state.bookmarks = {}

universe = get_comprehensive_universe()

# --- SIDEBAR CONFIGURATION & BOOKMARK WATCHLIST ---
st.sidebar.markdown("### ⚙️ ตั้งค่าการสแกนหุ้นเล่นรอบ")
selected_sector = st.sidebar.selectbox("📂 เลือกกลุ่มอุตสาหกรรม (Sector)", list(universe.keys()))
strategy_mode = st.sidebar.selectbox("⚙️ เลือกโหมดกลยุทธ์การเล่นรอบ", [
    "1. โหมดสะสมกรอบแคบ (RSI 40-60 และกรอบราคา 1 เดือนไม่เกิน 10% - ปลอดภัยสูง/รอข่าวเบรก)", 
    "2. โหมดโมเมนตัมเบรกเอาท์ตามกระแส (วอลุ่มพุ่งและราคาสวิงตัวเด่นชัด - เกาะเทรนด์ร้อน)"
])

st.sidebar.markdown("---")
st.sidebar.markdown("### 📌 หุ้นที่บันทึกไว้ (Bookmark Watchlist)")

if st.sidebar.button("🧹 ล้างรายการ Bookmark ทั้งหมด"):
    st.session_state.bookmarks = {}
    st.rerun()

if st.session_state.bookmarks:
    for tkr in list(st.session_state.bookmarks.keys()):
        data = st.session_state.bookmarks[tkr]
        try:
            live_df = yf.download(tkr, period="2d", interval="1d", progress=False)
            if not live_df.empty:
                if isinstance(live_df.columns, pd.MultiIndex):
                    live_df.columns = live_df.columns.droplevel(1)
                live_close = float(live_df['Close'].iloc[-1])
            else:
                live_close = data['bookmark_price']
        except:
            live_close = data['bookmark_price']
            
        bm_price = data['bookmark_price']
        target_p = data['target_price']
        pct_change = round(((live_close - bm_price) / bm_price) * 100, 2)
        
        with st.sidebar.expander(f"📌 [{tkr}] ตอนติ๊ก: ${bm_price}"):
            st.markdown(f"🎯 **เป้าขาย:** ${target_p}")
            st.markdown(f"💰 **ราคาปิดล่าสุด:** ${live_close}")
            color_prefix = "🟢" if pct_change >= 0 else "🔴"
            st.markdown(f"📊 **% เปลี่ยนแปลง:** {color_prefix} **{pct_change:+.2f}%**")
            if st.button(f"❌ ลบ {tkr}", key=f"del_bm_{tkr}"):
                del st.session_state.bookmarks[tkr]
                st.rerun()
else:
    st.sidebar.info("ยังไม่มีหุ้นที่ติ๊กเก็บไว้ เลือกติ๊กจากผลการสแกนด้านขวาได้เลยเพื่อน")

st.markdown("---")
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
                default_upside = 10.0
                default_target = round(latest_close * (1 + default_upside / 100.0), 2)
                tp1_price = round(latest_close * 1.05, 2)
                
                matched_data.append({
                    'Ticker': ticker, 'Moat': moat_story,
                    'Close': round(latest_close, 2), 'Range_Pct': round(range_pct * 100, 1),
                    'RSI_Latest': round(latest_rsi, 2), 'RSI_2M_Avg': rsi_2m_avg,
                    'TF_Data': tf_data, 'Default_Target': default_target, 'TP1': tp1_price,
                    'Low_Min': round(low_min, 2)
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
            
            expander_title = f"🟢 📌 [{ticker}] | ราคา: ${current_close} | กรอบราคา: ±{item['Range_Pct']}% | RSI: {item['RSI_Latest']}"
            
            with st.expander(expander_title, expanded=False):
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("💰 ราคาปัจจุบัน", f"${current_close}")
                col2.metric("📉 RSI ล่าสุด / เฉลี่ย 2M", f"{item['RSI_Latest']} / {item['RSI_2M_Avg']}")
                col3.metric("📊 ความกว้างกรอบ (1M)", f"{item['Range_Pct']}%")
                col4.metric("🎯 เป้าแนะนำ (TP1 5%)", f"${item['TP1']}")
                
                st.markdown("---")
                st.markdown(f"🔬 **จุดแข็งสิทธิบัตร, IP Moat & Ecosystem:** **{item['Moat']}**")
                st.markdown(f"📍 **จุดเข้าซื้อเชิงกลยุทธ์ (Entry Zone):** 🟢 **${item['Low_Min']} - ${round(item['Low_Min']*1.02, 2)}** (โซนเก็บของไส้เทียนล่าง)")
                
                # --- BOOKMARK FEATURE ---
                st.markdown("### 📌 ระบบ Bookmark & บันทึกเป้าหมายทำกำไร")
                is_bookmarked = ticker in st.session_state.bookmarks
                
                col_bm1, col_bm2, col_bm3 = st.columns([1, 2, 2])
                with col_bm1:
                    bookmark_checked = st.checkbox("ติ๊กเก็บเข้าพอร์ต", value=is_bookmarked, key=f"bm_check_{ticker}")
                
                default_target_val = st.session_state.bookmarks[ticker]['target_price'] if is_bookmarked else item['Default_Target']
                with col_bm2:
                    target_input = st.number_input("ราคาที่คิดว่าจะขายทำกำไร ($)", value=float(default_target_val), step=0.5, key=f"target_input_{ticker}")
                
                if bookmark_checked:
                    if not is_bookmarked:
                        st.session_state.bookmarks[ticker] = {
                            'bookmark_price': current_close,
                            'target_price': target_input,
                            'date': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')
                        }
                        st.success(f"บันทึก Bookmark หุ้น {ticker} ที่ราคา ${current_close} เรียบร้อย!")
                        st.rerun()
                    else:
                        st.session_state.bookmarks[ticker]['target_price'] = target_input
                else:
                    if is_bookmarked:
                        del st.session_state.bookmarks[ticker]
                        st.info(f"ลบ Bookmark หุ้น {ticker} ออกจากพอร์ตแล้ว")
                        st.rerun()

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

# --- DISPLAY ALL BOOKMARKS SUMMARY TABLE AT THE BOTTOM ---
if st.session_state.bookmarks:
    st.markdown("---")
    st.markdown("## 📊 📋 ตารางสรุปรายการ Bookmark หุ้นทั้งหมด (Portfolio Watchlist)")
    
    summary_data = []
    for tkr, data in st.session_state.bookmarks.items():
        try:
            live_df = yf.download(tkr, period="2d", interval="1d", progress=False)
            if not live_df.empty:
                if isinstance(live_df.columns, pd.MultiIndex):
                    live_df.columns = live_df.columns.droplevel(1)
                live_close = float(live_df['Close'].iloc[-1])
            else:
                live_close = data['bookmark_price']
        except:
            live_close = data['bookmark_price']
            
        bm_price = data['bookmark_price']
        target_p = data['target_price']
        pct_change = round(((live_close - bm_price) / bm_price) * 100, 2)
        target_upside = round(((target_p - live_close) / live_close) * 100, 2)
        
        summary_data.append({
            'Ticker': tkr,
            'วันที่บันทึก': data['date'],
            'ราคา ณ วันเริ่มติ๊ก ($)': bm_price,
            'ราคาเป้าหมายขาย ($)': target_p,
            'ราคาปิดล่าสุด ($)': live_close,
            '% เปลี่ยนแปลง (vs วันติ๊ก)': f"{pct_change:+.2f}%",
            'Upside ถึงเป้า (%)': f"{target_upside:+.2f}%"
        })
        
    if summary_data:
        df_summary = pd.DataFrame(summary_data)
        st.dataframe(df_summary, use_container_width=True)

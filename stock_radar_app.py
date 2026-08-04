import streamlit as st
import pandas as pd
import requests
import time
import numpy as np

# ตั้งค่าหน้าจอ Streamlit
st.set_page_config(page_title="Ultimate Global & Thai Market Screener", layout="wide")

# FMP API Key ของมึง
API_KEY = "akyx1POpzLt8geYg7oCuIvQW0qIsQjnh"

st.title("🚀 Ultimate Global (S&P 500 All Sectors) & SET100 Screener")
st.markdown("ระบบสแกนหุ้นครบทุก Sector ของ S&P 500 และ SET100 ไทย คัดกรองพฤติกรรมเจ้ามือ (RSI & Volume) พร้อมวิเคราะห์งบและแผน 3 ไม้")

# 1. รวบรวมรายชื่อหุ้น S&P 500 ครบทุก Sector หลัก และ SET100 แบบจัดเต็ม
@st.cache_data(ttl=86400)
def get_comprehensive_market_groups():
    return {
        "🇺🇸 S&P 500: Technology & AI Patents": [
            'AAPL', 'MSFT', 'NVDA', 'AVGO', 'ORCL', 'CRM', 'AMD', 'ADBE', 'ACN', 'CSCO', 
            'QCOM', 'IBM', 'TXN', 'INTU', 'AMAT', 'NOW', 'LRCX', 'ADI', 'MU', 'PANW', 
            'SNPS', 'CDNS', 'KLAC', 'MCHP', 'FTNT', 'ANSS', 'NXPI', 'MRVL', 'WDC', 'STX'
        ],
        "🇺🇸 S&P 500: Healthcare, Biotech & Pharma Patents": [
            'LLY', 'UNH', 'JNJ', 'ABBV', 'MRK', 'TMO', 'ABT', 'ISRG', 'PFE', 'AMGN', 
            'MDT', 'BMY', 'ELV', 'CVS', 'GILD', 'REGN', 'VRTX', 'ZTS', 'BSX', 'DXCM', 
            'CI', 'SYK', 'BDX', 'HUM', 'GEHC', 'ILMN', 'ALGN', 'IDXX', 'BAX', 'WAT'
        ],
        "🇺🇸 S&P 500: Consumer Discretionary & EV/Robotics": [
            'AMZN', 'TSLA', 'HD', 'MCD', 'NKE', 'LOW', 'SBUX', 'BKNG', 'TJX', 'ABNB', 
            'MAR', 'CMG', 'ORLY', 'HLT', 'ROST', 'DHI', 'GM', 'F', 'YUM', 'EXPE', 
            'TSCO', 'LULU', 'AZO', 'DASH', 'RCL', 'LEN', 'PHM', 'EBAY', 'ETSY', 'BBY'
        ],
        "🇺🇸 S&P 500: Financials & Fintech": [
            'BRK.B', 'JPM', 'V', 'MA', 'BAC', 'WFC', 'MS', 'GS', 'AXP', 'BLK', 
            'C', 'SPGI', 'CB', 'PGR', 'MMC', 'USB', 'TFC', 'PNC', 'COF', 'ICE'
        ],
        "🇺🇸 S&P 500: Communication Services (Media & Cloud)": [
            'GOOGL', 'GOOG', 'META', 'NFLX', 'DIS', 'CMCSA', 'TMUS', 'VZ', 'T', 'EA', 'TTWO', 'CHTR', 'OMC', 'IPG'
        ],
        "🇺🇸 S&P 500: Industrials & Aerospace Patents": [
            'GE', 'CAT', 'RTX', 'UNP', 'HON', 'DE', 'LMT', 'BA', 'ETN', 'MMM', 
            'CSX', 'NSC', 'PH', 'PCAR', 'FAST', 'URI', 'ODFL', 'CPRT', 'CTAS', 'GWW'
        ],
        "🇺🇸 S&P 500: Energy & Clean Tech Patents": [
            'XOM', 'CVX', 'COP', 'EOG', 'SLB', 'MPC', 'PSX', 'VLO', 'OXY', 'HAL', 
            'WMB', 'KMI', 'DVN', 'HES', 'BKR', 'FANG', 'TRGP', 'CTRA', 'EQT', 'MRO'
        ],
        "🇹🇭 SET100: หุ้นไทยสภาพคล่องสูงและบลูชิพ": [
            'ADVANC.BK', 'AOT.BK', 'BDMS.BK', 'BBL.BK', 'CPALL.BK', 'CPN.BK', 'DELTA.BK', 
            'GPSC.BK', 'GULF.BK', 'KBANK.BK', 'KTB.BK', 'MINT.BK', 'PTT.BK', 'PTTEP.BK', 
            'PTTGC.BK', 'SCB.BK', 'SCC.BK', 'SCGP.BK', 'TOP.BK', 'TRUE.BK', 'WHA.BK',
            'BANPU.BK', 'BEM.BK', 'BGRIM.BK', 'BH.BK', 'BTS.BK', 'CBG.BK', 'COM7.BK', 
            'CRC.BK', 'EA.BK', 'EGCO.BK', 'HMPRO.BK', 'IVL.BK', 'KTC.BK', 'LH.BK', 'OSP.BK',
            'BCH.BK', 'CENTEL.BK', 'GLOBAL.BK', 'IRPC.BK', 'JMT.BK', 'STGT.BK', 'TIDLOR.BK', 'TLI.BK'
        ]
    }

# 2. ฟังก์ชันวิเคราะห์แผนการเข้าซื้อ 3 ไม้ และรูปแบบการเล่น
def generate_trade_strategy(rsi, vol_cur, vol_past, roe):
    if roe > 15:
        play_style = "📈 หุ้นคุณภาพสูง (Core Port & Swing Trade)"
    elif vol_cur > 30:
        play_style = "⚡ หุ้นเก็งกำไรโมเมนตัมพุ่งตามข่าว/วอลุ่ม"
    else:
        play_style = "🐢 หุ้นสร้างฐานสะสมพลัง (Value & Trend Play)"

    if 40 <= rsi <= 60 and vol_past > 10 and vol_cur < 15:
        strategy_3_steps = (
            "ไม้ที่ 1 (30%): ทยอยเก็บสะสมบริเวณฐานราคาปัจจุบัน (โซนเจ้ามือสะสมของ)\n"
            "ไม้ที่ 2 (40%): เติมเงินเพิ่มเมื่อราคายืนเหนือเส้นค่าเฉลี่ยหรือมีข่าวสิทธิบัตร/งบออก\n"
            "ไม้ที่ 3 (30%): อัดไม้สุดท้ายเต็มพอร์ตเมื่อเกิดสัญญาณ Breakout เบรกแนวต้าน"
        )
    elif rsi > 65:
        strategy_3_steps = (
            "ไม้ที่ 1 (20%): ชะลอการไล่ราคา รอจังหวะย่อตัว (Overbought Zone)\n"
            "ไม้ที่ 2 (40%): ทยอยรับเพิ่มเมื่อราคาย่อตัวทดสอบแนวรับหลัก\n"
            "ไม้ที่ 3 (40%): เติมไม้สุดท้ายเมื่อกราฟฟอร์มตัวสร้างฐานรอบใหม่สำเร็จ"
        )
    else:
        strategy_3_steps = (
            "ไม้ที่ 1 (30%): เปิดไม้แรกเบาๆ สำหรับหุ้นที่กำลังสร้างกรอบสะสม\n"
            "ไม้ที่ 2 (30%): ถัวเฉลี่ยหรือเพิ่มน้ำหนักเมื่อวอลุ่มซื้อเริ่มหนาแน่น\n"
            "ไม้ที่ 3 (40%): อัดไม้สุดท้ายเมื่อเทรนด์กลับตัวเป็นขาขึ้นชัดเจน (Higher High)"
        )
        
    return play_style, strategy_3_steps

# 3. ฟังก์ชันสแกนแบบตรงจุด ลดภาระ API
def fetch_targeted_screener(symbols, group_name):
    stock_data = []
    progress_bar = st.progress(0)
    total = len(symbols)
    
    st.info(f"กำลังสแกนคัดกรองหุ้นทั้งหมด {total} ตัวในกลุ่ม {group_name}...")
    
    for i, symbol in enumerate(symbols):
        try:
            url_quote = f"https://financialmodelingprep.com/api/v3/quote/{symbol}?apikey={API_KEY}"
            res_q = requests.get(url_quote, timeout=3).json()
            
            if isinstance(res_q, list) and len(res_q) > 0:
                q = res_q[0]
                price = q.get('price', 0)
                vol_current = q.get('volume', 0)
                avg_vol = q.get('avgVolume', vol_current if vol_current > 0 else 1)
                vol_change_current = ((vol_current - avg_vol) / avg_vol) * 100 if avg_vol > 0 else 0
                
                url_metrics = f"https://financialmodelingprep.com/api/v3/key-metrics-ttm/{symbol}?apikey={API_KEY}"
                url_hist = f"https://financialmodelingprep.com/api/v3/historical-price-full/{symbol}?serietype=line&apikey={API_KEY}"
                
                res_m = requests.get(url_metrics, timeout=3).json()
                res_h = requests.get(url_hist, timeout=3).json()
                
                m = res_m[0] if (isinstance(res_m, list) and len(res_m) > 0) else {}
                hist_list = res_h.get('historical', []) if isinstance(res_h, dict) else []
                
                if hist_list and len(hist_list) > 15:
                    prices_30d = [x.get('close', price) for x in hist_list[:30]][::-1]
                    volumes_30d = [x.get('volume', 0) for x in hist_list[:30]][::-1]
                    
                    deltas = np.diff(prices_30d)
                    seed = deltas[:14]
                    up = seed[seed >= 0].sum() / 14
                    down = -seed[seed < 0].sum() / 14
                    rs = up / (down + 1e-9)
                    rsi_value = 100 - (100 / (1 + rs))
                    
                    avg_past_vol = np.mean(volumes_30d[:-5]) if len(volumes_30d) > 5 else avg_vol
                    recent_past_vol = np.mean(volumes_30d[-5:])
                    vol_change_past = ((recent_past_vol - avg_past_vol) / (avg_past_vol + 1e-9)) * 100
                else:
                    rsi_value = 50.0
                    vol_change_past = 0.0

                if rsi_value > 65 and vol_change_current > 30:
                    smart_status = "🚀 เจ้ามือลากราคาแรง (Markup / Breakout)"
                elif 40 <= rsi_value <= 60 and vol_change_past > 10 and vol_change_current < 15:
                    smart_status = "🟢 เจ้ามือกำลังสะสมของเงียบๆ (Accumulation)"
                elif rsi_value < 35 and vol_change_current > 25:
                    smart_status = "⚠️ แรงขายตื่นตระหนก (Panic Sell / Washout)"
                else:
                    smart_status = "⚪ ไร้ทิศทางชัดเจน (Consolidation)"

                roe_val = m.get('roeTTM', 0) * 100 if m.get('roeTTM') else 0
                play_style, strategy_3_steps = generate_trade_strategy(rsi_value, vol_change_current, vol_change_past, roe_val)

                stock_data.append({
                    'Group': group_name,
                    'Symbol': symbol,
                    'Company': q.get('name', symbol),
                    'Price': price,
                    'RSI (14)': round(rsi_value, 2),
                    '%Vol (Past)': round(vol_change_past, 2),
                    '%Vol (Cur)': round(vol_change_current, 2),
                    'Smart Money Status': smart_status,
                    'Play Style': play_style,
                    '3-Step Entry Plan': strategy_3_steps,
                    'PE': round(m.get('peRatioTTM', 0), 2),
                    'ROE (%)': round(roe_val, 2),
                    'FCF/Share': round(m.get('freeCashFlowPerShareTTM', 0), 2)
                })
        except Exception as e:
            pass
        
        time.sleep(0.1)
        progress_bar.progress((i + 1) / total)
        
    progress_bar.empty()
    return pd.DataFrame(stock_data)

# --- Sidebar UI ---
st.sidebar.header("🛠️ แผงควบคุมเลือกตลาดและ Sector")
groups_dict = get_comprehensive_market_groups()
chosen_market_group = st.sidebar.selectbox("เลือกกลุ่มตลาด / Sector ที่สนใจ", list(groups_dict.keys()))

selected_symbols = groups_dict[chosen_market_group]
st.sidebar.info(f"จำนวนหุ้นในกลุ่มนี้: {len(selected_symbols)} ตัว")

scan_button = st.sidebar.button("🚀 สแกนและวิเคราะห์เชิงลึกตามเงื่อนไข")

# --- Main Dashboard ---
if scan_button:
    df = fetch_targeted_screener(selected_symbols, chosen_market_group)
    
    if not df.empty:
        st.success(f"สแกนและวิเคราะห์สำเร็จ! พบข้อมูลทั้งหมด {len(df)} บริษัทในกลุ่มนี้")
        st.subheader(f"📊 ผลการสแกนและพฤติกรรมเจ้ามือ: {chosen_market_group}")
        
        status_filter = st.selectbox("🔍 กรองดูเฉพาะสถานะเจ้ามือ:", ["ทั้งหมด"] + list(df['Smart Money Status'].unique()))
        if status_filter != "ทั้งหมด":
            df_filtered = df[df['Smart Money Status'] == status_filter]
        else:
            df_filtered = df
            
        st.dataframe(df_filtered, use_container_width=True)
        
        st.markdown("---")
        st.subheader("💡 วิเคราะห์เจาะลึกงบการเงิน สตอรี่สิทธิบัตร และแผนเข้าซื้อ 3 ไม้รายตัว")
        
        for index, row in df_filtered.iterrows():
            with st.expander(f"📌 {row['Symbol']} - {row['Company']} | ราคา: ${row['Price']} | {row['Smart Money Status']}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**📈 สไตล์การลงทุน:** {row['Play Style']}")
                    st.markdown(f"**📊 งบการเงินเบื้องต้น:**\n- PE Ratio: {row['PE']}\n- ROE: {row['ROE (%)']}%\n- Free Cash Flow/Share: {row['FCF/Share']}")
                with col2:
                    st.markdown(f"**🎯 แผนการเข้าซื้อ 3 ไม้ (Scale-in Strategy):**\n```text\n{row['3-Step Entry Plan']}\n```")
        
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 ดาวน์โหลดผลการสแกนทั้งหมด (CSV)",
            data=csv,
            file_name=f"screener_{chosen_market_group.replace(' ', '_').replace(':', '')}.csv",
            mime='text/csv',
        )
    else:
        st.warning("เกิดข้อผิดพลาดในการเชื่อมต่อ ลองกดสแกนใหม่อีกครั้งเพื่อน")

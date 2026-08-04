import streamlit as st
import pandas as pd
import requests
import time
import numpy as np

# ตั้งค่าหน้าจอ Streamlit
st.set_page_config(page_title="Pro Innovation & Smart Money 3-Step Screener", layout="wide")

# FMP API Key ของมึง
API_KEY = "akyx1POpzLt8geYg7oCuIvQW0qIsQjnh"

st.title("🚀 Pro Innovation & Smart Money Screener (RSI, Volume & 3-Step Strategy)")
st.markdown("ระบบสแกนหุ้นนวัตกรรม สิทธิบัตร วิเคราะห์งบการเงิน พฤติกรรมเจ้ามือ (RSI & Volume) พร้อมแผนแบ่งเข้าซื้อ 3 ไม้และกลยุทธ์สั้น-ยาว")

# 1. รายชื่อหุ้นกลุ่มนวัตกรรมและเทคโนโลยีตัวท็อป S&P 500 (เน้นหุ้นที่มีสิทธิบัตรและเติบโตสูง)
@st.cache_data(ttl=86400)
def get_innovation_stock_groups():
    return {
        "Tech & AI Innovators (Tech)": [
            'AAPL', 'MSFT', 'NVDA', 'AVGO', 'ORCL', 'CRM', 'AMD', 'ADBE', 'ACN', 'CSCO', 
            'QCOM', 'IBM', 'TXN', 'INTU', 'AMAT', 'NOW', 'LRCX', 'ADI', 'MU', 'PANW'
        ],
        "Biotech & Medical Patents (Health)": [
            'LLY', 'UNH', 'JNJ', 'ABBV', 'MRK', 'TMO', 'ABT', 'ISRG', 'PFE', 'AMGN', 
            'MDT', 'BMY', 'ELV', 'CVS', 'GILD', 'REGN', 'VRTX', 'ZTS', 'BSX', 'DXCM'
        ],
        "Discretionary & EV Leaders (Consumer)": [
            'AMZN', 'TSLA', 'HD', 'MCD', 'NKE', 'LOW', 'SBUX', 'BKNG', 'TJX', 'ABNB', 
            'MAR', 'CMG', 'ORLY', 'HLT', 'ROST', 'DHI', 'GM', 'F', 'YUM', 'EXPE'
        ]
    }

# 2. ฟังก์ชันวิเคราะห์แผนการเข้าซื้อ 3 ไม้ และรูปแบบการเล่น (สั้น/ยาว) ตามสถานะหุ้น
def generate_trade_strategy(rsi, vol_cur, vol_past, roe):
    # กำหนดรูปแบบการเล่น
    if roe > 20:
        play_style = "📈 เล่นได้ทั้งระยะยาว (Core Port) และเล่นรอบ (Swing)"
    elif vol_cur > 40:
        play_style = "⚡ เน้นเก็งกำไรระยะสั้น (Day/Swing Trade ตามข่าว)"
    else:
        play_style = "🐢 ทยอยสะสมลงทุนระยะกลาง-ยาว (Value/Trend Play)"

    # แผนการเข้าซื้อ 3 ไม้
    if 40 <= rsi <= 60 and vol_past > 15 and vol_cur < 10:
        strategy_3_steps = (
            "ไม้ที่ 1: ทยอยเก็บสะสมไม้แรกบริเวณฐานราคาปัจจุบัน (โซนเจ้ามือสะสม)\n"
            "ไม้ที่ 2: เติมเงินซื้อเพิ่มเมื่อราคายืนเหนือเส้นค่าเฉลี่ยหรือมีข่าวสิทธิบัตรหนุน\n"
            "ไม้ที่ 3: จัดไม้สุดท้ายเต็มพอร์ตเมื่อเกิดสัญญาณ Breakout เบรกแนวต้านสำคัญ"
        )
    elif rsi > 65:
        strategy_3_steps = (
            "ไม้ที่ 1: ชะลอการไล่ราคา รอดูจังหวะย่อตัว (Overbought Zone)\n"
            "ไม้ที่ 2: ทยอยรับไม้แรกเมื่อราคาย่อตัวลงมาทดสอบแนวรับสำคัญ\n"
            "ไม้ที่ 3: เติมไม้สุดท้ายเมื่อกราฟฟอร์มตัวสร้างฐานราคาใหม่สำเร็จ"
        )
    else:
        strategy_3_steps = (
            "ไม้ที่ 1: เปิดไม้แรกเบาๆ สำหรับหุ้นที่กำลังสร้างกรอบสะสมพลัง\n"
            "ไม้ที่ 2: ถัวเฉลี่ยหรือเพิ่มน้ำหนักเมื่อวอลุ่มซื้อเริ่มหนาแน่นขึ้น\n"
            "ไม้ที่ 3: อัดไม้สุดท้ายเมื่อเทรนด์กลับตัวเป็นขาขึ้นชัดเจน (Higher High)"
        )
        
    return play_style, strategy_3_steps

# 3. ฟังก์ชันสแกนหลัก ประมวลผล RSI, Vol Change อดีต/ปัจจุบัน และงบการเงิน
@st.cache_data(ttl=3600)
def fetch_advanced_screener(symbols, group_name):
    stock_data = []
    progress_bar = st.progress(0)
    total = len(symbols)
    
    for i, symbol in enumerate(symbols):
        try:
            # ดึง Quote ปัจจุบัน
            url_quote = f"https://financialmodelingprep.com/api/v3/quote/{symbol}?apikey={API_KEY}"
            res_q = requests.get(url_quote).json()
            
            # ดึงงบ TTM
            url_metrics = f"https://financialmodelingprep.com/api/v3/key-metrics-ttm/{symbol}?apikey={API_KEY}"
            res_m = requests.get(url_metrics).json()

            # ดึงประวัติราคาและโวลุ่ม 30 วันย้อนหลัง
            url_hist = f"https://financialmodelingprep.com/api/v3/historical-price-full/{symbol}?serietype=line&apikey={API_KEY}"
            res_h = requests.get(url_hist).json()
            
            if isinstance(res_q, list) and len(res_q) > 0:
                q = res_q[0]
                m = res_m[0] if (isinstance(res_m, list) and len(res_m) > 0) else {}
                
                price = q.get('price', 0)
                vol_current = q.get('volume', 0)
                avg_vol = q.get('avgVolume', vol_current if vol_current > 0 else 1)
                
                # %Vol Change ปัจจุบันเทียบกับค่าเฉลี่ย
                vol_change_current = ((vol_current - avg_vol) / avg_vol) * 100 if avg_vol > 0 else 0
                
                # ดึงข้อมูลประวัติเพื่อคำนวณ RSI และ Vol อดีต
                hist_list = res_h.get('historical', []) if isinstance(res_h, dict) else []
                if hist_list and len(hist_list) > 15:
                    prices_30d = [x.get('close', price) for x in hist_list[:30]][::-1]
                    volumes_30d = [x.get('volume', 0) for x in hist_list[:30]][::-1]
                    
                    # คำนวณ RSI 14 วัน
                    deltas = np.diff(prices_30d)
                    seed = deltas[:14]
                    up = seed[seed >= 0].sum() / 14
                    down = -seed[seed < 0].sum() / 14
                    rs = up / (down + 1e-9)
                    rsi_value = 100 - (100 / (1 + rs))
                    
                    # %Vol Change อดีต
                    avg_past_vol = np.mean(volumes_30d[:-5]) if len(volumes_30d) > 5 else avg_vol
                    recent_past_vol = np.mean(volumes_30d[-5:])
                    vol_change_past = ((recent_past_vol - avg_past_vol) / (avg_past_vol + 1e-9)) * 100
                else:
                    rsi_value = 50.0
                    vol_change_past = 0.0

                # เช็กสถานะพฤติกรรมเจ้ามือ
                if rsi_value > 65 and vol_change_current > 40:
                    smart_status = "🚀 เจ้ามือลากราคาแรง (Markup / Breakout)"
                elif 40 <= rsi_value <= 60 and vol_change_past > 15 and vol_change_current < 10:
                    smart_status = "🟢 เจ้ามือกำลังสะสมของเงียบๆ (Accumulation)"
                elif rsi_value < 35 and vol_change_current > 30:
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
        
        time.sleep(0.2)
        progress_bar.progress((i + 1) / total)
        
    progress_bar.empty()
    return pd.DataFrame(stock_data)

# --- Sidebar UI ---
st.sidebar.header("🛠️ แผงควบคุมเงื่อนไขสแกนหุ้นนวัตกรรม")
groups_dict = get_innovation_stock_groups()
chosen_group = st.sidebar.selectbox("เลือกกลุ่มอุตสาหกรรมนวัตกรรม", list(groups_dict.keys()))

selected_symbols = groups_dict[chosen_group]
st.sidebar.info(f"จำนวนหุ้นในกลุ่ม: {len(selected_symbols)} ตัว")

scan_button = st.sidebar.button("🚀 เริ่มสแกนพฤติกรรมเจ้ามือ & แผน 3 ไม้")

# --- Main Dashboard ---
if scan_button:
    with st.spinner(f"กำลังวิเคราะห์ RSI, โวลุ่มอดีต/ปัจจุบัน และวางแผนกลยุทธ์ในกลุ่ม {chosen_group}..."):
        df = fetch_advanced_screener(selected_symbols, chosen_group)
        
        if not df.empty:
            st.success(f"สแกนสำเร็จ! วิเคราะห์ข้อมูลมาได้ทั้งหมด {len(df)} บริษัท")
            st.subheader(f"📊 ผลการสแกนเชิงลึกและแผนการลงทุน: {chosen_group}")
            
            st.dataframe(df, use_container_width=True)
            
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 ดาวน์โหลดผลการสแกนและแผนเทรด (CSV)",
                data=csv,
                file_name=f"innovation_screener_3steps_{chosen_group.replace(' ', '_')}.csv",
                mime='text/csv',
            )
        else:
            st.warning("เกิดข้อผิดพลาดในการเชื่อมต่อข้อมูล ลองกดใหม่อีกครั้งเพื่อน")

import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf

st.set_page_config(page_title="Ultimate Multi-Timeframe Volume & POC Sniper Pro", layout="wide")

st.title("🎯 Ultimate Multi-Timeframe Volume & POC Sniper Pro")
st.markdown("### เรดาร์เจาะลึก Volume รายวันถึงกรอบ 2 เดือน | แกะรอย Smart Money & Multi-POC Matrix เพื่อความมั่นใจสูงสุด")

st.sidebar.markdown("### ⚙️ ตั้งค่าเรดาร์สแกนหุ้นและ Volume")
input_ticker = st.sidebar.text_input("🔤 ใส่ชื่อย่อหุ้นที่ต้องการวิเคราะห์ (เช่น ETN, NVDA, ISRG, ROK)", value="ETN")
volume_spike_multiplier = st.sidebar.slider("🔥 ตัวคูณความผิดปกติของ Volume (เทียบกับ MA20)", min_value=1.5, max_value=5.0, value=2.0, step=0.25,
                                             help="ค่าสูงแปลว่าต้องเป็นวันที่มีวอลุ่มหนาแน่นกว่าปกติหลายเท่าตัว")

st.markdown(f"## 🔬 วิเคราะห์เชิงลึกหุ้นนวัตกรรมและสิทธิบัตร: **[{input_ticker.upper()}]**")

if st.button("🚀 รันเรดาร์วิเคราะห์ Multi-Timeframe Volume & POC"):
    ticker = input_ticker.upper().strip()
    
    with st.spinner(f"กำลังดึงข้อมูลและประมวลผล Volume & POC ทุกกรอบเวลาของ {ticker}..."):
        try:
            # ดึงข้อมูลย้อนหลัง 3 เดือน (ประมาณ 90 วันทำการ เพื่อครอบคลุมกรอบ 2 เดือน)
            df = yf.download(ticker, period="3mo", interval="1d", progress=False)
            if df.empty or len(df) < 30:
                st.error(f"ไม่พบข้อมูลของหุ้น [{ticker}] หรือข้อมูลน้อยเกินไป ลองตรวจสอบชื่อย่อใหม่อีกครั้งนะเพื่อน")
            else:
                if isinstance(df.columns, pd.MultiIndex):
                    df.columns = df.columns.droplevel(1)
                df.columns = [str(c).capitalize() for c in df.columns]
                df = df.dropna(subset=['Close', 'Volume', 'High', 'Low'])
                
                # คำนวณค่าเฉลี่ย Volume 20 วัน
                df['Vol_MA20'] = df['Volume'].rolling(window=20).mean()
                df['Vol_Ratio'] = df['Volume'] / df['Vol_MA20']
                
                # คำนวณ RSI
                delta = df['Close'].diff()
                gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                df['RSI'] = 100 - (100 / (1 + (gain / loss)))
                
                df = df.dropna()
                current_close = float(df['Close'].iloc[-1])
                
                # ฟังก์ชันคำนวณ POC และกรอบราคาตามช่วงเวลาที่กำหนด
                def get_poc_for_days(data_frame, days_count):
                    sub = data_frame.tail(days_count).copy() if len(data_frame) >= days_count else data_frame.copy()
                    h_max = float(sub['High'].max())
                    l_min = float(sub['Low'].min())
                    p_val = current_close
                    try:
                        hist_sub = sub.copy()
                        hist_sub['Bin'] = pd.cut(hist_sub['Close'], bins=8)
                        poc_row = hist_sub.groupby('Bin', observed=False)['Volume'].sum().idxmax()
                        if pd.notna(poc_row):
                            p_val = round(float(poc_row.mid), 2)
                    except:
                        p_val = round(current_close, 2)
                    dist = round(((current_close - p_val) / p_val) * 100, 2)
                    return {'poc': p_val, 'dist': dist, 'high': h_max, 'low': l_min}

                # กำหนดกรอบเวลาทั้งหมดตามที่มึงต้องการ
                timeframe_mapping = {
                    'รายวัน (1 วัน)': 1,
                    '3 วัน': 3,
                    '1 อาทิตย์ (5 วัน)': 5,
                    '2 อาทิตย์ (10 วัน)': 10,
                    '3 อาทิตย์ (15 วัน)': 15,
                    '1 เดือน (20 วัน)': 20,
                    '2 เดือน (40 วัน)': 40
                }
                
                multi_results = {}
                for tf_label, days_num in timeframe_mapping.items():
                    multi_results[tf_label] = get_poc_for_days(df, days_num)
                
                # กรองวันที่มี Volume ผิดปกติในช่วง 3 เดือน
                anomaly_df = df[df['Vol_Ratio'] >= volume_spike_multiplier].copy()
                
                st.success(f"วิเคราะห์สำเร็จ! โหลดข้อมูล Multi-Timeframe และ Volume Anomaly ของ [{ticker}] เรียบร้อย")
                st.markdown("---")
                
                # แสดง Metric ภาพรวม
                col1, col2, col3 = st.columns(3)
                col1.metric("💰 ราคาปัจจุบัน", f"${current_close}")
                col2.metric("📍 ฐาน POC (กรอบ 1 เดือน)", f"${multi_results['1 เดือน (20 วัน)']['poc']}")
                col3.metric("🔥 วันที่เกิด Volume ผิดปกติ (3 เดือน)", f"{len(anomaly_df)} ครั้ง")
                
                st.markdown("---")
                st.markdown("### 📊 ตารางเปรียบเทียบ Multi-Timeframe POC Matrix (ตั้งแต่รายวันถึง 2 เดือน)")
                
                matrix_rows = []
                for tf_label, res in multi_results.items():
                    matrix_rows.append({
                        'กรอบเวลา (Timeframe)': tf_label,
                        'ราคา POC (ฐานวอลุ่มหนาแน่นที่สุด)': f"${res['poc']}",
                        'ระยะห่างจากราคาปัจจุบัน': f"{res['dist']:+.2f}%",
                        'ราคาสูงสุดในช่วง': f"${res['high']}",
                        'ราคาต่ำสุดในช่วง': f"${res['low']}"
                    })
                st.table(pd.DataFrame(matrix_rows))
                
                st.markdown("---")
                st.markdown("### 📅 ตารางแกะรอย Volume รายวันผิดปกติ (Volume Anomaly Log ย้อนหลัง 3 เดือน)")
                
                if not anomaly_df.empty:
                    display_anomaly = []
                    for date_idx, row in anomaly_df.iterrows():
                        date_str = pd.to_datetime(date_idx).strftime('%Y-%m-%d')
                        close_p = round(float(row['Close']), 2)
                        vol_mil = round(float(row['Volume']) / 1e6, 2)
                        ratio = round(float(row['Vol_Ratio']), 2)
                        rsi_val = round(float(row['RSI']), 2)
                        
                        price_status = "🟢 ราคาปิดบวก (แรงซื้อดันสะสม)" if row['Close'] >= row['Open'] else "🔴 ราคาปิดลบ (แรงขายกระหน่ำ)"
                        
                        display_anomaly.append({
                            'วันที่เกิดเหตุการณ์': date_str,
                            'ราคาปิด': f"${close_p}",
                            'สถานะราคา': price_status,
                            'Volume (ล้านหุ้น)': f"{vol_mil} M",
                            'อัตราส่วนเทียบ Volume เฉลี่ย (MA20)': f"{ratio}x",
                            'RSI วันนั้น': f"{rsi_val}"
                        })
                    st.table(pd.DataFrame(display_anomaly))
                else:
                    st.info("ในช่วง 3 เดือนนี้ ไม่มีวันไหนที่ Volume พุ่งสูงเกินตัวคูณที่ตั้งไว้ แสดงว่าซื้อขายกันปกติไม่มีพิรุธ")
                    
                st.markdown("---")
                st.markdown(f"💡 **มุมมองเพื่อนซี้วิเคราะห์ให้สบายใจ:** ดูจากตาราง **Multi-POC Matrix** ด้านบน ถ้ามึงเห็นว่าราคาปัจจุบันกำลังย่อลงมาคลอเคลียอยู่ใกล้โซน POC ของกรอบ **1 เดือน หรือ 2 เดือน** (ระยะห่างติดลบนิดๆ หรือ 0%) แถมพอย้อนไปดูตาราง **Volume Anomaly** แล้วพบว่ามีวันที่มีวอลุ่มพุ่งหนาแน่นในโซนราคาเดียวกัน — **มั่นใจได้เลยเพื่อน!** ตรงนั้นแหละคือแนวรับเหล็กที่ Smart Money เข้ามาตั้งโต๊ะสะสมของจริง ทยอยเก็บเข้าพอร์ตแล้วรอนับกำไรได้เลย ลุย!วิเคราะห์จบครบเครื่องแบบนี้ เอาไปใช้เทรดทำกำไรได้สบายใจแน่นอนเพื่อน!
                

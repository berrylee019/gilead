import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# --- [0] 기본 설정 및 스타일 ---
st.set_page_config(page_title="Gilead Clinical AI Suite", layout="wide", page_icon="🧬")

st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    [data-testid="stSidebar"] { background-color: #ffffff; }
    </style>
    """, unsafe_allow_html=True)

# --- [1] Global Clinical Suite 함수들 (내용 복구) ---

def show_adc_optimizer():
    st.header(" ADC Toxicity & Efficacy Predictor")
    st.info("항체와 페이로드 조합에 따른 치료 창(Therapeutic Window)을 시뮬레이션합니다.")
    
    col_input, col_display = st.columns([1, 2])
    with col_input:
        st.subheader("Parameters")
        antibody = st.selectbox("Antibody Target", ["Sacituzumab (TROP-2)", "Trastuzumab (HER2)", "Gadiratuzumab"])
        payload = st.selectbox("Payload Type", ["SN-38", "DXd", "MMAE"])
        dar = st.slider("Drug-to-Antibody Ratio (DAR)", 1.0, 8.0, 4.0)
        
    with col_display:
        eff = (dar * 12) + (len(antibody) * 1.5)
        tox = (dar ** 2.1) + (len(payload) * 3)
        c1, c2 = st.columns(2)
        c1.metric("Predicted Efficacy", f"{eff:.1f}%", delta="High")
        c2.metric("Predicted Toxicity", f"{tox:.1f}%", delta="-Low", delta_color="inverse")
        
        chart_data = pd.DataFrame({
            'DAR': np.linspace(1, 8, 20),
            'Efficacy': np.linspace(1, 8, 20) * 10 + 5,
            'Toxicity': (np.linspace(1, 8, 20) ** 2.1)
        })
        fig = px.line(chart_data, x='DAR', y=['Efficacy', 'Toxicity'], 
                      title="Efficacy vs Toxicity Trade-off", template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)

def show_equity_analyzer():
    st.header(" Global Trial Equity & Risk Dashboard")
    df = pd.DataFrame({
        'City': ['Seoul', 'New York', 'London', 'Tokyo', 'Sao Paulo'],
        'lat': [37.56, 40.71, 51.50, 35.68, -23.55],
        'lon': [126.97, -74.00, -0.12, 139.65, -46.63],
        'Enrollment': [150, 300, 120, 200, 180],
        'Diversity Score': [0.65, 0.92, 0.85, 0.70, 0.88]
    })
    fig = px.scatter_geo(df, lat='lat', lon='lon', hover_name='City', size='Enrollment',
                         color='Diversity Score', projection="natural earth",
                         color_continuous_scale=px.colors.sequential.Reds)
    fig.update_geos(showcountries=True, showocean=True, oceancolor="LightBlue")
    st.plotly_chart(fig, use_container_width=True)

def show_protocol_intelligence():
    st.header(" Clinical Protocol Intelligence")
    uploaded_file = st.file_uploader("임상 프로토콜 PDF 업로드", type="pdf")
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "안녕하세요, 프로토콜 분석을 도와드릴까요?"}]
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])
    if prompt := st.chat_input("질문을 입력하세요"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        with st.chat_message("assistant"):
            response = "분석 결과, 본 임상의 제외 기준 4.2.1에 해당합니다."
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

# --- [2] Gilead Korea Edition 함수들 ---

def show_k_multi_center_tracker():
    st.header("🇰🇷 국내 다기관 실시간 협업 맵")
    k_hospitals = pd.DataFrame({
        'Hospital': ['서울대병원', '삼성서울병원', '서울아산병원', '세브란스병원', '국립암센터'],
        'lat': [37.5796, 37.4882, 37.5266, 37.5611, 37.7777],
        'lon': [127.0001, 127.0851, 127.1084, 126.9407, 126.7765],
        'Target': [50, 50, 45, 40, 30],
        'Actual': [42, 38, 41, 28, 15]
    })
    k_hospitals['Enrollment Rate (%)'] = (k_hospitals['Actual'] / k_hospitals['Target'] * 100).round(1)
    fig = px.scatter_mapbox(k_hospitals, lat="lat", lon="lon", hover_name="Hospital", 
                            size="Actual", color="Enrollment Rate (%)",
                            color_continuous_scale=px.colors.sequential.OrRd, zoom=10, height=500)
    fig.update_layout(mapbox_style="carto-positron")
    st.plotly_chart(fig, use_container_width=True)

def show_patient_funnel():
    st.header(" 환자 스크리닝 & 탈락 분석 퍼널")
    funnel_data = pd.DataFrame({"Stage": ["Pre-Screened", "Logged", "Eligible", "Enrolled"], "Count": [1200, 450, 180, 155]})
    st.plotly_chart(px.funnel(funnel_data, x='Count', y='Stage'), use_container_width=True)

def show_safety_ae_monitoring():
    st.header(" 실시간 안전성 알람 & 호중구 감소증 관리")
    days = np.arange(0, 22, 1)
    anc_values = 3500 - (2500 * np.exp(-(days-8)**2 / 10)) 
    fig = px.line(x=days, y=anc_values, labels={'x':'Day', 'y':'ANC (cells/mm³)'}, title="Patient ID: K-001 Trend")
    fig.add_hline(y=1000, line_dash="dash", line_color="red", annotation_text="Danger (1000)")
    st.plotly_chart(fig, use_container_width=True)
    st.error("🚨 **K-001 환자 고위험**: 호중구 수치가 급격히 하락 중입니다. 투여 주의 요망.")

# --- [3] 메인 사이드바 내비게이션 ---

#st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/f/fb/Gilead_Sciences_logo.svg/512px-Gilead_Sciences_logo.svg.png", width=180)
#st.sidebar.info("")
category = st.sidebar.selectbox("Select Suite", ["Global Clinical Suite", "Gilead Korea Edition"])
#st.sidebar.markdown("---")
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2864/2864248.png", width=60)
    st.title("MisaTech AI")
    st.markdown("---")
    
if category == "Global Clinical Suite":
    app_mode = st.sidebar.radio("Global Tools", ["ADC Optimizer", "Equity Analyzer", "Protocol Intelligence"])
else:
    app_mode = st.sidebar.radio("Korea Edition", ["K-Multi-Center Tracker", "Patient Funnel", "Safety & AE Monitoring"])

# --- [4] 페이지 렌더링 로직 ---

if category == "Global Clinical Suite":
    if app_mode == "ADC Optimizer": show_adc_optimizer()
    elif app_mode == "Equity Analyzer": show_equity_analyzer()
    elif app_mode == "Protocol Intelligence": show_protocol_intelligence()
else:
    if app_mode == "K-Multi-Center Tracker": show_k_multi_center_tracker()
    elif app_mode == "Patient Funnel": show_patient_funnel()
    elif app_mode == "Safety & AE Monitoring": show_safety_ae_monitoring()

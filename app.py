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
    st.header("🧪 ADC Toxicity & Efficacy Predictor (Trodelvy Optimized)")
    
    col_input, col_display = st.columns([1, 2])
    with col_input:
        st.subheader("Parameters")
        # 트로델비의 항체 타겟인 TROP-2를 기본값으로 설정
        antibody = st.selectbox("Antibody Target", ["Sacituzumab (TROP-2)", "Trastuzumab (HER2)", "Gadiratuzumab"])
        # 트로델비의 페이로드인 SN-38을 기본값으로 설정
        payload = st.selectbox("Payload Type", ["SN-38", "DXd", "MMAE"])
        # 트로델비의 실제 평균 DAR은 약 7.6으로 매우 높습니다. 슬라이더 범위를 조절합니다.
        dar = st.slider("Drug-to-Antibody Ratio (DAR)", 1.0, 10.0, 7.6)
        
    with col_display:
        # --- 트로델비 특화 예측 로직 (가상) ---
        # SN-38은 독성이 상대적으로 낮아 높은 DAR(7.6)이 가능함을 반영
        if payload == "SN-38":
            eff = (dar * 11) + 10  # 약효는 안정적으로 상승
            tox = (dar ** 1.8) + 5  # 독성 상승 곡선이 MMAE보다 완만함
        else:
            eff = (dar * 12) + 5
            tox = (dar ** 2.2) + 10

        c1, c2 = st.columns(2)
        c1.metric("Predicted Efficacy", f"{eff:.1f}%", delta="Target Reach")
        c2.metric("Predicted Toxicity", f"{tox:.1f}%", delta="-Safe Range", delta_color="inverse")
        
        # 그래프 데이터 생성
        x_range = np.linspace(1, 10, 50)
        if payload == "SN-38":
            y_eff = (x_range * 11) + 10
            y_tox = (x_range ** 1.8) + 5
        else:
            y_eff = (x_range * 12) + 5
            y_tox = (x_range ** 2.2) + 10

        chart_data = pd.DataFrame({'DAR': x_range, 'Efficacy': y_eff, 'Toxicity': y_tox})
        fig = px.line(chart_data, x='DAR', y=['Efficacy', 'Toxicity'], 
                      title=f"{antibody} + {payload} 시뮬레이션 결과",
                      color_discrete_map={'Efficacy': '#C80037', 'Toxicity': '#646569'})
        
        # 현재 선택한 DAR 위치에 수직선 표시 (현실적인 최적점 확인용)
        fig.add_vline(x=dar, line_dash="dot", line_color="blue", annotation_text=f"Current DAR {dar}")
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
#st.sidebar.markdown("---")
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2864/2864248.png", width=60)
    st.title("MisaTech AI")
    st.markdown("---")

category = st.sidebar.selectbox("Select Suite", ["Global Clinical Suite", "Gilead Korea Edition"])
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

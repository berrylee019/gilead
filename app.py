import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import pydeck as pdk

# --- [0] 기본 설정 및 스타일 ---
st.set_page_config(page_title="Gilead Clinical AI Suite", layout="wide", page_icon="🧬")

# 길리어드 느낌의 스타일링 (옵션)
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# --- [1] 도구별 함수 정의 ---

def show_adc_optimizer():
    st.header("🧪 ADC Toxicity & Efficacy Predictor")
    st.info("항체와 페이로드 조합에 따른 치료 창(Therapeutic Window)을 시뮬레이션합니다.")
    
    col_input, col_display = st.columns([1, 2])
    
    with col_input:
        st.subheader("Parameters")
        antibody = st.selectbox("Antibody Target", ["Sacituzumab (TROP-2)", "Trastuzumab (HER2)", "Gadiratuzumab"])
        payload = st.selectbox("Payload Type", ["SN-38", "DXd", "MMAE"])
        dar = st.slider("Drug-to-Antibody Ratio (DAR)", 1.0, 8.0, 4.0)
        
    with col_display:
        # 가상 예측 로직
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
    st.header("📊 Trial Equity & Risk Dashboard")
    st.write("전 세계 임상 사이트의 환자 모집 현황과 다양성 지표를 모니터링합니다.")
    
    # 가상 데이터
    df = pd.DataFrame({
        'city': ['Seoul', 'New York', 'London', 'Tokyo', 'Sao Paulo'],
        'lat': [37.56, 40.71, 51.50, 35.68, -23.55],
        'lon': [126.97, -74.00, -0.12, 139.65, -46.63],
        'enrollment': [150, 300, 120, 200, 180],
        'diversity_score': [0.65, 0.92, 0.85, 0.70, 0.88]
    })
    
    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=pdk.ViewState(latitude=20, longitude=0, zoom=1),
        layers=[
            pdk.Layer('ScatterplotLayer', data=df, get_position='[lon, lat]',
                      get_color='[0, 104, 201, 160]', get_radius='enrollment * 2000')
        ],
    ))
    
    st.subheader("Site Compliance Status")
    cols = st.columns(len(df))
    for i, row in df.iterrows():
        status = "✅" if row['diversity_score'] >= 0.8 else "⚠️"
        cols[i].write(f"**{row['city']}**")
        cols[i].write(f"{status} {int(row['diversity_score']*100)}%")

def show_protocol_intelligence():
    st.header("💬 Clinical Protocol Intelligence")
    st.write("LLM(Gemini)을 활용하여 복잡한 임상 프로토콜 문서를 즉시 분석합니다.")
    
    uploaded_file = st.file_uploader("임상 프로토콜 PDF 업로드", type="pdf")
    
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "안녕하세요, 형님! 업로드하신 프로토콜에 대해 궁금한 점을 물어봐 주세요."}]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("질문을 입력하세요 (예: 이 임상의 HER2 관련 제외 기준은?)"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            # 실제 구현 시 Gemini API 호출 로직이 들어가는 곳
            response = "분석 결과, 본 임상의 4.2.1절에 따르면 HER2 IHC 3+ 환자는 본 코호트에서 제외되지만, HER2-low 그룹에는 참여가 가능합니다."
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

# --- [2] 메인 사이드바 내비게이션 ---

st.sidebar.image("https://www.gilead.com/-/media/gilead-corporate/images/logos/gilead_logo_red_white.png", width=150) # 로고 예시
st.sidebar.title("Navigation")
app_mode = st.sidebar.radio("Select Tool", 
    ["ADC Optimizer", "Trial Equity Analyzer", "Protocol Intelligence"])

st.sidebar.markdown("---")
st.sidebar.write(f"**User:** 형님(Hyung-nim)")
st.sidebar.write(f"**System Status:** Operational ✅")

# --- [3] 페이지 렌더링 ---

if app_mode == "ADC Optimizer":
    show_adc_optimizer()
elif app_mode == "Trial Equity Analyzer":
    show_equity_analyzer()
elif app_mode == "Protocol Intelligence":
    show_protocol_intelligence()
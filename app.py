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
    </style>
    """, unsafe_allow_html=True)

# --- [1] Korea Edition 전용 함수 ---

def show_k_multi_center_tracker():
    st.header("🇰🇷 국내 다기관 실시간 협업 맵")
    st.write("한국 내 주요 거점 병원별 임상 진행 현황을 실시간으로 트래킹합니다.")
    
    # 국내 주요 병원 좌표 및 데이터
    k_hospitals = pd.DataFrame({
        'Hospital': ['서울대병원', '삼성서울병원', '서울아산병원', '세브란스병원', '국립암센터'],
        'lat': [37.5796, 37.4882, 37.5266, 37.5611, 37.7777],
        'lon': [127.0001, 127.0851, 127.1084, 126.9407, 126.7765],
        'Target': [50, 50, 45, 40, 30],
        'Actual': [42, 38, 41, 28, 15]
    })
    k_hospitals['Enrollment Rate (%)'] = (k_hospitals['Actual'] / k_hospitals['Target'] * 100).round(1)

    col1, col2 = st.columns([2, 1])
    
    with col1:
        # 한국 중심 지도 시각화
        fig = px.scatter_mapbox(k_hospitals, lat="lat", lon="lon", hover_name="Hospital", 
                                size="Actual", color="Enrollment Rate (%)",
                                color_continuous_scale=px.colors.sequential.OrRd,
                                zoom=10, height=500)
        fig.update_layout(mapbox_style="carto-positron")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Site Performance")
        st.dataframe(k_hospitals[['Hospital', 'Target', 'Actual', 'Enrollment Rate (%)']], hide_index=True)

def show_patient_funnel():
    st.header("📉 환자 스크리닝 & 탈락 분석 퍼널")
    st.write("스크리닝 단계별 환자 유실 원인을 분석하여 임상 효율을 극대화합니다.")
    
    # 퍼널 데이터
    funnel_data = pd.DataFrame({
        "Stage": ["Pre-Screened", "Screening Logged", "Eligible", "Enrolled/Randomized"],
        "Count": [1200, 450, 180, 155]
    })
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.funnel(funnel_data, x='Count', y='Stage', title="Enrollment Funnel")
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        st.subheader("Screening Failure Reasons")
        fail_reasons = pd.DataFrame({
            "Reason": ["Lab Criteria (ANC/Liver)", "Inclusion/Exclusion", "Consent Withdrawal", "Prior Therapy Violation"],
            "Value": [45, 25, 15, 10]
        })
        fig_pie = px.pie(fail_reasons, values='Value', names='Reason', hole=0.4)
        st.plotly_chart(fig_pie, use_container_width=True)

def show_safety_ae_monitoring():
    st.header("⚠️ 실시간 안전성 알람 & 호중구 감소증 관리")
    st.info("트로델비(ADC) 투여 환자의 호중구 수치(ANC)를 집중 모니터링하여 독성을 선제적으로 관리합니다.")

    # 환자별 호중구 수치 가상 데이터
    days = np.arange(0, 22, 1)
    # ANC 수치 시뮬레이션 (Cycle 1 투여 후 7~10일째 최저점 형성)
    anc_values = 3500 - (2500 * np.exp(-(days-8)**2 / 10)) 
    
    st.subheader("Patient ANC(Absolute Neutrophil Count) Trend")
    chart_data = pd.DataFrame({"Day": days, "ANC (cells/mm³)": anc_values})
    
    fig = px.line(chart_data, x="Day", y="ANC (cells/mm³)", title="Trial Patient ID: K-001 (Cycle 1)")
    # 가이드라인 표시
    fig.add_hline(y=1500, line_dash="dash", line_color="orange", annotation_text="Grade 1 (1500)")
    fig.add_hline(y=1000, line_dash="dash", line_color="red", annotation_text="Grade 2 (1000)")
    fig.add_hline(y=500, line_dash="dash", line_color="darkred", annotation_text="Grade 3/4 (500)")
    
    st.plotly_chart(fig, use_container_width=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.error("🚨 **K-001 환자 고위험 알람**: Day 8-10 구간 Grade 3 호중구 감소증 예상. G-CSF(성장인자) 투여 혹은 용량 조절 검토 필요.")
    with col2:
        st.success("✅ **K-005 환자 정상**: 현재 ANC 2,200 유지 중. 차주 투여 일정 정상 진행 가능.")

# --- [2] 기존 Global 도구 함수 (생략/유지) ---
def show_adc_optimizer(): st.header("🧪 ADC Toxicity & Efficacy Predictor")
def show_equity_analyzer(): st.header("📊 Global Trial Equity & Risk")
def show_protocol_intelligence(): st.header("💬 Protocol Intelligence")

# --- [3] 메인 사이드바 내비게이션 (이원화) ---

st.sidebar.image("https://gilead.stylelabs.cloud/api/public/content/89749f3b535e4eebb8ae07c8e9607b17?v=c1371898", width=150)

# 카테고리 선택
category = st.sidebar.selectbox("Select Suite", ["Global Clinical Suite", "Gilead Korea Edition"])

st.sidebar.markdown("---")

if category == "Global Clinical Suite":
    app_mode = st.sidebar.radio("Global Tools", ["ADC Optimizer", "Equity Analyzer", "Protocol Intelligence"])
else:
    app_mode = st.sidebar.radio("Korea Edition", ["K-Multi-Center Tracker", "Patient Funnel", "Safety & AE Monitoring"])

st.sidebar.markdown("---")
st.sidebar.write(f"**Current User:** PI / Coordinator (형님)")
st.sidebar.write(f"**Region:** South Korea 🇰🇷")

# --- [4] 페이지 렌더링 로직 ---

if category == "Global Clinical Suite":
    if app_mode == "ADC Optimizer": show_adc_optimizer()
    elif app_mode == "Equity Analyzer": show_equity_analyzer()
    elif app_mode == "Protocol Intelligence": show_protocol_intelligence()
else:
    if app_mode == "K-Multi-Center Tracker": show_k_multi_center_tracker()
    elif app_mode == "Patient Funnel": show_patient_funnel()
    elif app_mode == "Safety & AE Monitoring": show_safety_ae_monitoring()

# app.py
# Streamlit 근로장려금 계산기 – 2024년 버전 (재산 + 기한후신고 반영)
# 실행: streamlit run app.py

import streamlit as st
import pandas as pd

st.set_page_config(page_title="2024년 근로장려금 계산기", page_icon="💰", layout="centered")

st.title("💰 2024년 근로장려금 계산기")
st.caption("비공식 참고용 계산기 • 국세청 홈택스 공식 결과와 다를 수 있습니다.")

with st.expander("ℹ️ 계산 기준 안내", expanded=False):
    st.markdown("""
    - 2024년 귀속 근로장려금 기준으로 작성된 간이 계산기입니다.  
    - 가구유형별 최대 지급액과 총소득 상한은 **국세청 공개자료**를 기반으로 합니다.  
    - **재산 1억 4천만 원 초과~2억 4천만 원 이하**: 지급액의 50% 감액  
      **2억 4천만 원 초과**: 지급 제외(재산기준 초과)  
    - **기한 후 신청 시** 지급액의 **90%**만 지급됩니다.
    """)

# ------------------------------
# 1️⃣ 기준 파라미터 (2024년 귀속)
# ------------------------------
PARAMS = {
    "단독":   {"max": 1_650_000, "upper_income": 22_000_000, "phase_in_start": 4_000_000,  "peak_start": 9_000_000,  "peak_end": 14_000_000},
    "홑벌이": {"max": 2_850_000, "upper_income": 32_000_000, "phase_in_start": 7_000_000,  "peak_start": 14_000_000, "peak_end": 21_000_000},
    "맞벌이": {"max": 3_300_000, "upper_income": 44_000_000, "phase_in_start": 8_000_000,  "peak_start": 17_000_000, "peak_end": 26_000_000},
}

# ------------------------------
# 2️⃣ 사용자 입력
# ------------------------------
col1, col2 = st.columns(2)
with col1:
    hh_type = st.selectbox("가구유형", options=["단독", "홑벌이", "맞벌이"])
with col2:
    income = st.number_input("연간 총소득(원)", value=10_000_000, step=100_000, min_value=0)

property_value = st.number_input("재산가액(원)", value=50_000_000, step=1_000_000, min_value=0)
late_filing = st.checkbox("기한 후 신고 여부", value=False, help="체크 시 지급액이 10% 감액됩니다.")

st.divider()

# ------------------------------
# 3️⃣ 근로장려금 계산 함수
# ------------------------------
def calc_eitc(income: int, params: dict) -> int:
    """소득에 따른 근로장려금 계산 (선형 근사)"""
    max_amt = params["max"]
    s = params["phase_in_start"]
    peak_start = params["peak_start"]
    peak_end = params["peak_end"]
    upper = params["upper_income"]

    if income < s:
        return 0
    if s <= income < peak_start:
        span = peak_start - s
        return int(max_amt * (income - s) / span)
    if peak_start <= income <= peak_end:
        return int(max_amt)
    if peak_end < income < upper:
        span = upper - peak_end
        return int(max_amt * (upper - income) / span)
    return 0

def apply_property_adjustment(amount: int, prop: int) -> tuple[int, str]:
    """재산 기준 감액 또는 제외"""
    if prop <= 140_000_000:
        return amount, "정상 지급"
    elif 140_000_000 < prop <= 240_000_000:
        return int(amount * 0.5), "재산기준 감액(50%)"
    else:
        return 0, "재산기준 초과(미지급)"

def apply_late_filing_adjustment(amount: int, is_late: bool) -> tuple[int, str]:
    """기한 후 신고 감액"""
    if not is_late:
        return amount, ""
    return int(amount * 0.9), "기한 후 신고 감액(10%)"

# ------------------------------
# 4️⃣ 계산 로직
# ------------------------------
params = PARAMS[hh_type]
base_amount = calc_eitc(income, params)
prop_adjusted, prop_note = apply_property_adjustment(base_amount, property_value)
final_amount, late_note = apply_late_filing_adjustment(prop_adjusted, late_filing)

# ------------------------------
# 5️⃣ 결과 출력
# ------------------------------
st.subheader("📊 계산 결과")
st.metric(label="예상 근로장려금 지급액", value=f"{final_amount:,.0f} 원")

# 결과 상태 요약
notes = []
if prop_note != "정상 지급":
    notes.append(prop_note)
if late_filing:
    notes.append(late_note)
if not notes:
    notes = ["정상 지급"]

st.write("💬 지급유형: **" + " / ".join(notes) + "**")

with st.expander("📋 계산 상세"):
    st.write({
        "가구유형": hh_type,
        "총소득": f"{income:,} 원",
        "재산가액": f"{property_value:,} 원",
        "기한후신고": "예" if late_filing else "아니오",
        "기본 산정액": f"{base_amount:,} 원",
        "재산 조정 후": f"{prop_adjusted:,} 원",
        "최종 지급액": f"{final_amount:,} 원",
        "지급 판정": " / ".join(notes),
    })

st.divider()
st.markdown("""
**참고 기준 (2024년 귀속)**  
- 단독: 총소득 2,200만 원 미만 / 최대 165만 원  
- 홑벌이: 총소득 3,200만 원 미만 / 최대 285만 원  
- 맞벌이: 총소득 4,400만 원 미만 / 최대 330만 원  
- 재산 1.4억~2.4억: 지급액의 50% 감액  
- 재산 2.4억 초과: 지급 제외  
- 기한 후 신고: 지급액의 10% 감액
""")

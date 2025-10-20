import streamlit as st

# -----------------------------
# 근로장려금 계산 함수
# -----------------------------
def calc_eitc(income: int, household_type: str, age: int) -> int:
    """
    소득구간별 근로장려금 계산
    """

    eitc_table = {
        '단독':  {'max': 1500000, 'max_start': 0, 'max_end': 400, 'reduce_start': 900, 'reduce_end': 2200},
        '홑벌이': {'max': 2600000, 'max_start': 0, 'max_end': 700, 'reduce_start': 1700, 'reduce_end': 3600},
        '맞벌이': {'max': 3000000, 'max_start': 0, 'max_end': 800, 'reduce_start': 2000, 'reduce_end': 4000}
    }

    if household_type not in eitc_table:
        raise ValueError("household_type은 '단독', '홑벌이', '맞벌이' 중 하나여야 합니다.")

    info = eitc_table[household_type]

    # 소득 단위 (만원 → 원)
    income_m = income

    # 구간별 계산
    if income_m <= info['max_end']:
        amount = info['max']
    elif income_m <= info['reduce_start']:
        amount = info['max']
    elif income_m <= info['reduce_end']:
        # 선형 감액
        ratio = 1 - (income_m - info['reduce_start']) / (info['reduce_end'] - info['reduce_start'])
        amount = int(info['max'] * ratio)
    else:
        amount = 0

    # 65세 이상 추가 10%
    if age >= 65:
        amount = int(amount * 1.1)

    return max(amount, 0)


# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="근로장려금 계산기", page_icon="💰", layout="centered")

st.title("💰 근로장려금 계산기 (소득 구간별)")
st.markdown("**2025년 예시 기준 근로장려금 계산기**\n\n소득에 따라 감액되는 구조를 반영했습니다.")

st.divider()

col1, col2, col3 = st.columns(3)
with col1:
    age = st.number_input("나이", min_value=18, max_value=100, value=40)
with col2:
    household = st.selectbox("가구 유형", ["단독", "홑벌이", "맞벌이"])
with col3:
    income = st.number_input("연소득 (만원 단위)", min_value=0, max_value=5000, value=1200)

if st.button("계산하기"):
    result = calc_eitc(income, household, age)
    if result > 0:
        st.success(f"👉 예상 근로장려금: **{result:,}원**")
        if age >= 65:
            st.info("※ 65세 이상이므로 10% 추가 혜택이 반영되었습니다.")
    else:
        st.warning("소득이 감액 종료구간을 초과하여 근로장려금을 받을 수 없습니다.")

st.divider()
st.caption("※ 본 계산기는 참고용입니다. 실제 지급액은 국세청 심사 결과에 따라 달라질 수 있습니다.")

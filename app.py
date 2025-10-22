import streamlit as st

st.set_page_config(page_title="고용증대 세액공제 계산기", page_icon="💼", layout="centered")

st.title("💼 고용증대 세액공제 계산기")
st.write("조세특례제한법 제29조의7에 따른 고용증대 세액공제를 간편하게 계산합니다.")

# 입력값 받기
st.header("📋 기본 정보 입력")

prev_employees = st.number_input("직전연도 상시근로자 수", min_value=0, value=50)
curr_employees = st.number_input("당해연도 상시근로자 수", min_value=0, value=60)
prev_young = st.number_input("직전연도 청년 상시근로자 수", min_value=0, value=10)
curr_young = st.number_input("당해연도 청년 상시근로자 수", min_value=0, value=15)

company_size = st.selectbox("기업 규모", ["중소기업", "중견기업", "대기업"])
location = st.selectbox("소재지", ["수도권", "지방"])

st.markdown("---")

# 계산 로직
def employment_increase_credit(
    prev_employees,
    curr_employees,
    prev_young,
    curr_young,
    company_size,
    location
):
    total_increase = curr_employees - prev_employees
    young_increase = curr_young - prev_young
    general_increase = total_increase - young_increase

    # 예시 단가 (단위: 만원)
    rates = {
        "중소기업": {"수도권": (700, 1200), "지방": (770, 1300)},
        "중견기업": {"수도권": (500, 900), "지방": (550, 1000)},
        "대기업": {"수도권": (400, 750), "지방": (450, 800)},
    }

    general_rate, young_rate = rates[company_size][location]

    credit = (general_increase * general_rate) + (young_increase * young_rate)
    return total_increase, young_increase, general_increase, credit

if st.button("🔍 세액공제 계산하기"):
    total_inc, young_inc, general_inc, credit = employment_increase_credit(
        prev_employees, curr_employees, prev_young, curr_young, company_size, location
    )

    st.success("✅ 계산 결과")
    st.write(f"- 총 상시근로자 증가 인원: **{total_inc}명**")
    st.write(f"- 청년 상시근로자 증가 인원: **{young_inc}명**")
    st.write(f"- 일반 상시근로자 증가 인원: **{general_inc}명**")
    st.write(f"💰 예상 세액공제액: **{credit:,.0f}만원**")

    st.caption("※ 실제 금액은 조세특례제한법 시행령 기준에 따라 변동될 수 있습니다.")

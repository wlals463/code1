import streamlit as st

st.title("💰 2025년 소득세 계산기")
st.write("연소득에 따른 소득세, 세율, 누진공제를 계산합니다.")

# 입력
income = st.number_input("연소득을 입력하세요 (원)", min_value=0, step=1000000, format="%d")

# 세율표
tax_brackets = [
    (12_000_000, 0.06, 0),
    (46_000_000, 0.15, 1_080_000),
    (88_000_000, 0.24, 5_220_000),
    (150_000_000, 0.35, 14_900_000),
    (300_000_000, 0.38, 19_400_000),
    (500_000_000, 0.40, 25_400_000),
    (1_000_000_000, 0.42, 35_400_000),
    (float('inf'), 0.45, 65_400_000)
]

# 계산 함수
def calculate_income_tax(income):
    for limit, rate, deduction in tax_brackets:
        if income <= limit:
            tax = income * rate - deduction
            return rate, deduction, max(0, round(tax))

# 계산 버튼
if st.button("세금 계산하기"):
    rate, deduction, tax = calculate_income_tax(income)
    st.subheader("🧾 계산 결과")
    st.write(f"**연소득:** {income:,.0f} 원")
    st.write(f"**적용 세율:** {rate*100:.0f}%")
    st.write(f"**누진공제액:** {deduction:,.0f} 원")
    st.write(f"**산출세액:** {tax:,.0f} 원")

    st.info(f"💡 지방소득세는 산출세액의 10%이며, 총 세액은 {tax * 1.1:,.0f} 원입니다.")

# 참고용 세율표
st.markdown("### 📊 세율표 (2025년 기준)")
st.table({
    "과세표준 구간 (원)": [
        "1,200만 이하", "1,200만 ~ 4,600만", "4,600만 ~ 8,800만", 
        "8,800만 ~ 1.5억", "1.5억 ~ 3억", "3억 ~ 5억", "5억 ~ 10억", "10억 초과"
    ],
    "세율": ["6%", "15%", "24%", "35%", "38%", "40%", "42%", "45%"],
    "누진공제": ["0", "1,080,000", "5,220,000", "14,900,000", "19,400,000", "25,400,000", "35,400,000", "65,400,000"]
})

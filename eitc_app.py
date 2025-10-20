import streamlit as st

# -----------------------------
# 근로장려금 계산 함수
# -----------------------------
def get_max_eitc(age: int, household_type: str) -> int:
    """
    근로장려금 최대 지급 가능액 계산기
    Parameters:
        age (int): 나이
        household_type (str): 가구 유형 ('단독', '홑벌이', '맞벌이')
    Returns:
        int: 근로장려금 최대 지급 가능액 (원)
    """

    base_amounts = {
        '단독': 1500000,   # 150만원
        '홑벌이': 2600000, # 260만원
        '맞벌이': 3000000  # 300만원
    }

    if household_type not in base_amounts:
        raise ValueError("household_type은 '단독', '홑벌이', '맞벌이' 중 하나여야 합니다.")

    # 65세 이상은 10% 추가
    bonus_rate = 1.1 if age >= 65 else 1.0

    return int(base_amounts[household_type] * bonus_rate)


# -----------------------------
# Streamlit UI 구성
# -----------------------------
st.set_page_config(page_title="근로장려금 계산기", page_icon="💰", layout="centered")

st.title("💰 근로장려금 최대 지급 가능액 계산기")
st.markdown("**국세청 근로장려금**을 간단하게 예측해보세요. (예시용 계산)")

st.divider()

# 입력 폼
age = st.number_input("나이를 입력하세요", min_value=18, max_value=100,_

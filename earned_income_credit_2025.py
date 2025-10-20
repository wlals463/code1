# filename: earned_income_credit_2025.py

def get_eitc_amount(income: int, household_type: str) -> int:
    """
    2025년 근로장려금 산정표(가정치 기준)
    household_type: "단독", "홑벌이", "맞벌이"
    income: 연간 총소득 (만원 단위)
    return: 근로장려금 지급액 (원 단위)
    """

    # 가구별 최대 지급액 및 구간 (2024년 기준)
    table = {
        "단독": {"max": 1650000, "min_income": 400, "peak_income": 900, "phaseout_income": 2200},
        "홑벌이": {"max": 2850000, "min_income": 700, "peak_income": 1400, "phaseout_income": 3200},
        "맞벌이": {"max": 3300000, "min_income": 800, "peak_income": 1700, "phaseout_income": 4400},
    }

    if household_type not in table:
        raise ValueError("가구 유형은 '단독', '홑벌이', '맞벌이' 중 하나여야 합니다.")

    t = table[household_type]
    inc = income

    # 구간별 산정 로직 (단순화된 버전)
    if inc < t["min_income"]:
        # 너무 낮은 소득은 미지급
        return 0
    elif inc <= t["peak_income"]:
        # 상승 구간: 소득이 증가할수록 장려금 증가
        return int(t["max"] * (inc - t["min_income"]) / (t["peak_income"] - t["min_income"]))
    elif inc <= t["phaseout_income"]:
        # 감액 구간: 소득이 높을수록 장려금 감소
        return int(t["max"] * (t["phaseout_income"] - inc) / (t["phaseout_income"] - t["peak_income"]))
    else:
        # 초과 시 미지급
        return 0


if __name__ == "__main__":
    print("=== 2025년 근로장려금 계산기 ===")
    gagu = input("가구 유형을 입력하세요 (단독 / 홑벌이 / 맞벌이): ").strip()
    income = int(input("연간 총소득(만원)을 입력하세요: "))

    amount = get_eitc_amount(income, gagu)
    print(f"\n예상 근로장려금 지급액: {amount:,}원")

import streamlit as st
import math

# =========================
# 1. 상수 정의
# =========================
emission_factor = {
    "전기": 450,      # g CO2 / 단위
    "난방유": 2660,
    "도시가스": 2000,
    "지역난방": 500,
    "LPG": 1500
}

# 이산화탄소 1톤(1,000,000 g) 당 편백나무 8그루 필요
GRAMS_PER_TON_CO2 = 1_000_000
TREES_PER_TON_CO2 = 8


# =========================
# 2. 함수 정의
# =========================
def calculate_emissions(amount, energy_type):
    """에너지 사용량 × 배출계수 (g 단위)"""
    if energy_type not in emission_factor:
        return None
    return amount * emission_factor[energy_type]

def evaluate_emission(emission_g):
    """총 배출량에 대한 간단 평가 (g 단위 기준)"""
    if emission_g < 1000:
        return "배출량이 매우 낮아요. 좋은 수준이에요!"
    elif emission_g < 5000:
        return "보통 수준의 배출량이에요."
    elif emission_g < 20000:
        return "배출량이 조금 높은 편이에요. 절약을 고려해도 좋아요."
    else:
        return "배출량이 매우 높습니다. 사용량 조절이 필요해요!"

def calculate_tree_count(emission_g):
    """
    emission_g : g 단위 CO2 배출량
    이산화탄소 1톤 당 편백나무 8그루 기준으로 필요한 나무 수(올림)
    """
    if emission_g <= 0:
        return 0
    tons = emission_g / GRAMS_PER_TON_CO2  # g → ton
    trees = math.ceil(tons * TREES_PER_TON_CO2)
    return trees


# =========================
# 3. Streamlit UI
# =========================
st.title("🌱 생활 에너지 탄소 배출 & 편백나무 계산기")

st.caption("기준: CO₂ 1톤(1,000,000 g) 당 편백나무 8그루 필요")

st.subheader("1️⃣ 에너지 사용량 입력")

# 에너지별 입력 (복잡하지 않게 세로로 배치)
amount_inputs = {}
for energy in emission_factor.keys():
    amount = st.number_input(
        f"{energy} 사용량",
        min_value=0.0,
        step=1.0,
        key=f"amount_{energy}"
    )
    amount_inputs[energy] = amount

# =========================
# 4. 계산 버튼
# =========================
if st.button("계산하기"):
    total_emission_g = 0
    detail_rows = []

    for energy, amount in amount_inputs.items():
        if amount > 0:
            emission_g = calculate_emissions(amount, energy)
            total_emission_g += emission_g
            tree_count = calculate_tree_count(emission_g)

            # 에너지별 결과(간단하게, 소수점 최소화)
            detail_rows.append({
                "에너지": energy,
                "사용량": int(amount) if amount.is_integer() else round(amount, 1),
                "배출량 (kg CO₂)": round(emission_g / 1000, 1),
                "편백나무(그루)": tree_count
            })

    if total_emission_g == 0:
        st.warning("최소 한 가지 에너지의 사용량을 0보다 크게 입력해주세요.")
    else:
        st.subheader("2️⃣ 총 결과")

        total_emission_kg = total_emission_g / 1000
        total_trees = calculate_tree_count(total_emission_g)

        # 소수점 깔끔하게 (kg은 1자리)
        col1, col2 = st.columns(2)
        with col1:
            st.metric("총 배출량", f"{total_emission_kg:,.1f} kg CO₂")
        with col2:
            st.metric("필요 편백나무 수", f"{total_trees} 그루")

        st.write("**총 배출량 평가:**", evaluate_emission(total_emission_g))

        # 🌳 이모지로 나무 보여주기
        st.markdown("### 🌳 편백나무를 눈으로 보기")

        max_trees_to_show = 50  # 화면 터지지 않게 최대 50개만 이모지 표시
        trees_to_show = min(total_trees, max_trees_to_show)

        if trees_to_show > 0:
            tree_line = "🌳" * trees_to_show
            st.write(tree_line)

            if total_trees > max_trees_to_show:
                st.write(f"... (실제 필요 편백나무는 총 **{total_trees}그루**)")
        else:
            st.write("필요한 편백나무 수가 거의 없어요 🍀")

        # 에너지별 자세한 정보는 접어서 보기 (복잡함 ↓)
        if detail_rows:
            with st.expander("에너지별 자세한 배출량 보기"):
                st.table(detail_rows)

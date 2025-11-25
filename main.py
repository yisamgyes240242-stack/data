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
    """에너지 사용량 × 배출계수"""
    if energy_type not in emission_factor:
        return None
    return amount * emission_factor[energy_type]

def evaluate_emission(emission):
    """총 배출량에 대한 간단 평가"""
    if emission < 1000:
        return "배출량이 매우 낮아요. 좋은 수준이에요!"
    elif emission < 5000:
        return "보통 수준의 배출량이에요."
    elif emission < 20000:
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
st.title("🌱 생활 에너지 탄소 배출 계산기 (편백나무 기준)")

st.write(
    """
여러 종류의 에너지 사용량을 한 번에 입력하면  
각 에너지별 탄소 배출량과 **총합**,  
그리고 이를 상쇄하기 위해 필요한 **편백나무 수**를 계산해 줍니다.

> 기준: **이산화탄소 1톤(1,000,000 g) 당 편백나무 8그루 필요**
"""
)

st.markdown("### 1️⃣ 에너지별 사용량 입력")

# 에너지별 입력 칸
amount_inputs = {}
cols = st.columns(len(emission_factor))

for idx, (energy, factor) in enumerate(emission_factor.items()):
    with cols[idx]:
        amount = st.number_input(
            f"{energy} 사용량",
            min_value=0.0,
            step=1.0,
            key=f"amount_{energy}"
        )
        amount_inputs[energy] = amount

# =========================
# 4. 버튼 클릭 시 계산
# =========================
if st.button("배출량 계산하기"):
    results = []
    total_emission = 0.0

    # 에너지별 배출량 계산
    for energy, amount in amount_inputs.items():
        if amount > 0:
            emission = calculate_emissions(amount, energy)
            total_emission += emission
            trees = calculate_tree_count(emission)

            results.append({
                "에너지": energy,
                "사용량": amount,
                "배출량 (g CO₂)": round(emission, 2),
                "필요 편백나무 수 (그루)": trees
            })

    if total_emission == 0:
        st.warning("최소 한 가지 에너지의 사용량을 0보다 크게 입력해주세요.")
    else:
        # 에너지별 결과표
        st.subheader("📊 에너지별 배출량 결과")
        st.table(results)

        # 총합 결과
        st.markdown("### 2️⃣ 총합 기준으로 보기")

        total_trees = calculate_tree_count(total_emission)
        total_tons = total_emission / GRAMS_PER_TON_CO2

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("총 탄소 배출량 (g CO₂)", f"{total_emission:,.0f}")
        with col2:
            st.metric("총 탄소 배출량 (톤 CO₂)", f"{total_tons:.4f}")
        with col3:
            st.metric("필요 편백나무 수", f"{total_trees} 그루")

        st.write("**총 배출량 평가:**", evaluate_emission(total_emission))

        st.markdown(
            f"""
- 이 배출량을 상쇄하려면  
  → **편백나무 약 `{total_trees}`그루**가 필요하다고 볼 수 있어요.  
- 기준: **CO₂ 1톤(1,000,000 g) 당 편백나무 8그루 필요**
"""
        )

        st.markdown("---")
        st.subheader("🌍 저탄소 생활 실천 방법")

        st.markdown(
            """
**1. 냉·난방 온도 적정 수준 유지하기**  
- 여름: **26℃ 이상**, 겨울: **20℃ 이하**  
- 냉난방 온도를 1℃ 조정하면  
  → **연간 약 110kg CO₂ 감소**,  
  → **냉난방 비용 약 34,000원 절약**

**2. 절전형 전등으로 교체하기**  
- 백열등(60W) → 형광등(24W) 교체 시  
  → 연간 **약 17kg CO₂ 감소**  
- 절전형 형광등은  
  → 백열등보다 **수명 약 8배**,  
  → **전력 소비도 더 적음**

**3. 걷기·자전거·대중교통 생활화하기**  
- 승용차 이용을 **일주일에 하루만 줄여도**  
  → 연간 **약 445kg CO₂ 감소**
"""
        )

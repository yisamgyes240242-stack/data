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
        return

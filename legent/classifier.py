from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class AccidentClassifier:
    """Rule-based accident classification."""

    def classify(self, info: Dict) -> Optional[str]:
        env = info.get("사고_발생_환경", {})
        veh_a = info.get("차량_A_정보", {})
        veh_b = info.get("차량_B_정보", {})

        # Example rule for 도표 201: A 직진 녹색, B 직진 적색, 사거리 교차로
        if (
            env.get("도로_유형") and "사거리" in env.get("도로_유형")
            and veh_a.get("진행_방향") == "직진"
            and veh_b.get("진행_방향") == "직진"
            and veh_a.get("신호등_상태") == "녹색"
            and veh_b.get("신호등_상태") == "적색"
        ):
            return "도표 201"

        # Additional rules can be implemented here

        return None

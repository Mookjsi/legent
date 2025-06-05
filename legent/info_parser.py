import json
import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class InformationParser:
    """Parse LVLM textual response to structured JSON."""

    schema: Dict = field(default_factory=lambda: {
        "사고_발생_환경": {
            "사고_발생_추정_시각": None,
            "기상_상태": None,
            "도로_유형": None,
            "교차로_종류": None,
            "도로_표면_상태": None,
            "차선_정보": None,
            "주변_교통_상황": None,
        },
        "차량_A_정보": {
            "차량_종류": None,
            "진행_방향": None,
            "사고_직전_속도": None,
            "신호등_상태": None,
            "방향지시등_작동_여부": None,
            "차선_준수_여부": None,
            "교차로_진입_방식": None,
            "충돌_부위": None,
            "기타_특이사항": None,
        },
        "차량_B_정보": {
            "차량_종류": None,
            "진행_방향": None,
            "사고_직전_속도": None,
            "신호등_상태": None,
            "방향지시등_작동_여부": None,
            "차선_준수_여부": None,
            "교차로_진입_방식": None,
            "충돌_부위": None,
            "기타_특이사항": None,
        },
        "사고_상황_기술": {
            "상호_작용_및_동선": None,
            "충돌_순간_상황": None,
            "주요_원인_추정": None,
            "PDF_용어_해당_여부": [],
        },
        "추가_관찰_사항": None,
    })

    def parse(self, text: str) -> Dict:
        """Parse text to a structured dict."""
        if not text:
            return json.loads(json.dumps(self.schema))

        data = json.loads(json.dumps(self.schema))

        def _extract(section: str, key: str) -> Optional[str]:
            pattern = rf"{key}\s*[:：]\s*(.+)"
            section_pattern = rf"{section}.*?(?:\n\n|\Z)"
            match_section = re.search(section_pattern, text, re.DOTALL)
            if not match_section:
                return None
            match_item = re.search(pattern, match_section.group(0))
            if match_item:
                return match_item.group(1).strip()
            return None

        for sec in ["사고 발생 환경", "차량 A 정보", "차량 B 정보", "사고 상황 기술", "추가 관찰 사항"]:
            for key in data[self._map_key(sec)]:
                val = _extract(sec, self._human_readable(key))
                if val is not None:
                    data[self._map_key(sec)][key] = val

        return data

    def _map_key(self, section: str) -> str:
        mapping = {
            "사고 발생 환경": "사고_발생_환경",
            "차량 A 정보": "차량_A_정보",
            "차량 B 정보": "차량_B_정보",
            "사고 상황 기술": "사고_상황_기술",
            "추가 관찰 사항": "추가_관찰_사항",
        }
        return mapping.get(section, section)

    def _human_readable(self, key: str) -> str:
        return key.replace('_', ' ')

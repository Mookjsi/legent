import os
import sys
import importlib.util
import pytest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
spec = importlib.util.spec_from_file_location(
    "info_parser", os.path.join(ROOT, "legent", "info_parser.py")
)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
InformationParser = module.InformationParser


def test_parse_basic():
    text = (
        "사고 발생 환경:\n"
        "사고 발생 추정 시각: 2023-10-10 10:00\n"
        "기상 상태: 맑음\n\n"
        "차량 A 정보:\n"
        "차량 종류: 승용차\n"
    )
    parser = InformationParser()
    result = parser.parse(text)
    assert result["사고_발생_환경"]["사고_발생_추정_시각"] == "2023-10-10 10:00"
    assert result["사고_발생_환경"]["기상_상태"] == "맑음"
    assert result["차량_A_정보"]["차량_종류"] == "승용차"


def test_parse_newline_variations():
    text = (
        "사고 발생 환경:\r\n"
        "사고 발생 추정 시각 :\r\n 12:00\r\n"
        "기상 상태 : 맑음\r\n\r\n"
        "차량 A 정보:\r\n"
        "차량 종류:\r\n 승용차\r\n"
    )
    parser = InformationParser()
    result = parser.parse(text)
    assert result["사고_발생_환경"]["사고_발생_추정_시각"] == "12:00"
    assert result["사고_발생_환경"]["기상_상태"] == "맑음"
    assert result["차량_A_정보"]["차량_종류"] == "승용차"

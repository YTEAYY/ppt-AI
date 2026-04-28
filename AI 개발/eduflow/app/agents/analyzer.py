# app/agents/analyzer.py
"""
콘텐츠 분석가 (Content Analyzer Agent)
======================================
역할: 사용자가 업로드한 학습 자료를 분석하여 핵심 내용을 추출하고
      발표용 구조를 생성합니다.

주요 기능:
1. 문서 요약 및 핵심 키워드 추출
2. PPT 슬라이드 구조(목차) 생성
3. 학습 목표 및 핵심 메시지 도출
"""

from app.services.openai_client import get_llm


def summarize_text(text: str) -> str:
    """문서 요약 + 핵심 키워드 추출."""
    llm = get_llm()
    
    if llm is None:
        # API 키가 없을 때 더미 응답
        return f"[요약] {text[:200]}..."
    
    prompt = f"""
    학교 과제/발표용 자료를 다음 형식으로 정리해 주세요:
    1. 핵심 주제 3개
    2. 각 주제에 대한 3개의 세부 포인트
    3. 학습 목표와 핵심 메시지

    자료:
    {text}
    """
    return llm.invoke(prompt)


def build_outline(text: str) -> str:
    """발표 슬라이드 구조(목차) 생성."""
    llm = get_llm()
    
    if llm is None:
        # API 키가 없을 때 기본 구조
        return "1. 서론\n2. 본론\n3. 결론"
    
    prompt = f"""
    아래 자료를 바탕으로 PPT 슬라이드 구조를 만들어 주세요.
    - 슬라이드 제목
    - 핵심 내용
    - 시각화 아이디어(이미지/차트 등)

    자료:
    {text}
    """
    return llm.invoke(prompt)

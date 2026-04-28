# app/agents/feedback.py
"""
피드백 에이전트 (Feedback Agent)
================================
역할: 학생들 간의 피드백을 수집하고 분석하여 개선점을 도출합니다.

주요 기능:
1. 피드백 텍스트 수집
2. 공통 이슈 및 개선점 분석
3. 요약 및 태그 생성
"""

from app.services.openai_client import get_llm


def collect_feedback(responses: list[dict]) -> str:
    """학생들이 제출한 피드백(텍스트)을 한글 요약과 태그로 정리."""
    llm = get_llm()
    
    if llm is None:
        # API 키가 없을 때 기본 응답
        return f"총 {len(responses)}개의 피드백이 수집되었습니다."
    
    prompt = f"""
    아래 학생 피드백들을 읽고 한 문장으로 요약하고, 개선 포인트 3가지를 제안해 주세요.
    피드백 리스트:
    {responses}
    """
    return llm.invoke(prompt)

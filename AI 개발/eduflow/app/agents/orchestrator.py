# app/agents/orchestrator.py
"""
Orchestrator - 멀티 에이전트 코디네이터
======================================
역할: 각 에이전트(analyzer, master, feedback)의 작업을 조정하고 
      워크플로우를 관리합니다.

주요 기능:
1. 콘텐츠 분석 → PPT 생성 → 피드백 수집 파이프라인 조율
2. 에이전트 간 데이터 흐름 관리
3. 에러 처리 및 재시도 로직
"""

from typing import Dict, Any, Optional
from pathlib import Path
import asyncio

from app.agents import analyzer, master, feedback
from app.services.openai_client import get_llm


class Orchestrator:
    """
    EduFlow의 코어 허브 - 모든 에이전트의 작업을 조정합니다.
    """
    
    def __init__(self):
        self.llm = get_llm()  # None일 수 있음
        self.status = "idle"
    
    async def process_upload(self, content: str, script: str, output_dir: Path) -> Dict[str, Any]:
        """
        전체 워크플로우 실행:
        1. 콘텐츠 분석 (analyzer)
        2. PPT 생성 (master)
        3. 결과 반환
        """
        self.status = "processing"
        
        try:
            # 1단계: 분석
            outline = await asyncio.to_thread(analyzer.build_outline, content)
            summarized = await asyncio.to_thread(analyzer.summarize_text, content)
            
            # 2단계: PPT 생성
            ppt_path = output_dir / f"{output_dir.name}.pptx"
            await asyncio.to_thread(master.generate_ppt, outline, script, ppt_path)
            
            self.status = "completed"
            
            return {
                "outline": outline,
                "script": summarized,
                "ppt_path": str(ppt_path),
                "status": "success"
            }
            
        except Exception as e:
            self.status = "error"
            return {
                "status": "error",
                "error": str(e)
            }
    
    async def process_feedback(self, responses: list) -> Dict[str, Any]:
        """
        피드백 처리 워크플로우:
        1. 학생 피드백 수집
        2. 요약 및 개선점 도출
        """
        self.status = "processing_feedback"
        
        try:
            summary = await asyncio.to_thread(feedback.collect_feedback, responses)
            
            self.status = "completed"
            
            return {
                "summary": summary,
                "status": "success"
            }
            
        except Exception as e:
            self.status = "error"
            return {
                "status": "error",
                "error": str(e)
            }
    
    def get_status(self) -> str:
        """현재 오케스트레이터 상태 반환"""
        return self.status


# 전역 인스턴스 - 지연 초기화
_orchestrator = None

def get_orchestrator() -> Orchestrator:
    """오케스트레이터 인스턴스 반환 (지연 초기화)"""
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = Orchestrator()
    return _orchestrator
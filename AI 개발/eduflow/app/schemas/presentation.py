# app/schemas/presentation.py
"""
PPT 생성 관련 Pydantic 스키마
============================
"""

from pydantic import BaseModel, Field
from typing import Optional, List


class SlideContent(BaseModel):
    """개별 슬라이드 내용"""
    title: str = Field(..., description="슬라이드 제목")
    content: str = Field(..., description="슬라이드 본문 내용")
    visualization: Optional[str] = Field(None, description="시각화 아이디어")


class OutlineRequest(BaseModel):
    """아웃라인 생성 요청"""
    content: str = Field(..., description="분석할 학습 자료 내용")
    num_slides: int = Field(default=5, description="생성할 슬라이드 수")


class OutlineResponse(BaseModel):
    """아웃라인 생성 응답"""
    slides: List[SlideContent] = Field(..., description="생성된 슬라이드 목록")
    summary: str = Field(..., description="전체 요약")
    keywords: List[str] = Field(..., description="핵심 키워드")


class PPTGenerateRequest(BaseModel):
    """PPT 생성 요청"""
    outline: str = Field(..., description="슬라이드 구조")
    script: str = Field(..., description="발표 대본")
    theme: Optional[str] = Field(default="school", description="테마 (school/business)")


class PPTGenerateResponse(BaseModel):
    """PPT 생성 응답"""
    ppt_path: str = Field(..., description="생성된 PPT 파일 경로")
    slide_count: int = Field(..., description="생성된 슬라이드 수")
    status: str = Field(default="success", description="처리 상태")
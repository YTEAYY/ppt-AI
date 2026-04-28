# app/schemas/upload.py
"""
업로드 관련 Pydantic 스키마
===========================
"""

from pydantic import BaseModel, Field
from typing import Optional


class UploadRequest(BaseModel):
    """파일 업로드 요청 스키마"""
    script: str = Field(..., description="발표 대본 또는 설명 텍스트")


class UploadResponse(BaseModel):
    """파일 업로드 응답 스키마"""
    outline: str = Field(..., description="생성된 PPT 슬라이드 구조")
    script: str = Field(..., description="요약된 문서 내용")
    ppt_path: str = Field(..., description="생성된 PPT 파일 경로")
    status: str = Field(default="success", description="처리 상태")


class FeedbackRequest(BaseModel):
    """피드백 요청 스키마"""
    responses: list[str] = Field(..., description="학생 피드백 목록")


class FeedbackResponse(BaseModel):
    """피드백 응답 스키마"""
    summary: str = Field(..., description="피드백 요약")
    status: str = Field(default="success", description="처리 상태")
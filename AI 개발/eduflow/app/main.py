# app/main.py
"""
EduFlow - 학교 맞춤형 발표 및 과제 자동화 AI
============================================
멀티 에이전트 아키텍처:
- Orchestrator: 코어 허브, 작업 조정
- Analyzer: 콘텐츠 분석 및 구조 생성
- Master: PPT 슬라이드 생성
- Feedback: 학생 피드백 수집 및 분석
"""

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path
import uuid
import shutil
import os
import asyncio

from app.agents import analyzer, master, feedback, orchestrator
from app.schemas.upload import UploadResponse, FeedbackRequest, FeedbackResponse

app = FastAPI(
    title="EduFlow API",
    description="학교 맞춤형 발표 및 과제 자동화 AI 플랫폼",
    version="1.0.0"
)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


# PPTX → PDF 변환 함수 (Windows + PowerPoint 필요)
def pptx_to_pdf(pptx_path: str, pdf_path: str):
    try:
        import comtypes.client
        powerpoint = comtypes.client.CreateObject("PowerPoint.Application")
        powerpoint.Visible = 1
        ppt = powerpoint.Presentations.Open(pptx_path, WithWindow=False)
        ppt.SaveAs(pdf_path, 32)  # 32 = PDF
        ppt.Close()
        powerpoint.Quit()
    except ImportError:
        raise RuntimeError(
            "PDF conversion requires comtypes and Microsoft PowerPoint (Windows only). "
            "Consider using LibreOffice for Linux-based environments."
        )


@app.post("/upload", response_model=UploadResponse)
async def upload(file: UploadFile = File(...), script: str = Form(...)):
    # 1) 파일 저장
    file_path = UPLOAD_DIR / f"{uuid.uuid4()}_{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 2) 분석 + 구조 생성 (async)
    content = file_path.read_text(encoding="utf-8")
    outline = await asyncio.to_thread(analyzer.build_outline, content)
    dscript = await asyncio.to_thread(analyzer.summarize_text, content)

    # 3) PPT 생성
    ppt_path = UPLOAD_DIR / f"{uuid.uuid4()}.pptx"
    await asyncio.to_thread(master.generate_ppt, outline, script, ppt_path)

    return UploadResponse(
        outline=outline,
        script=dscript,
        ppt_path=str(ppt_path),
        status="success"
    )


# PDF 다운로드 엔드포인트
@app.get("/download_pdf/{ppt_id}")
async def download_pdf(ppt_id: str):
    pptx_path = UPLOAD_DIR / f"{ppt_id}.pptx"
    pdf_path = UPLOAD_DIR / f"{ppt_id}.pdf"
    if not pptx_path.exists():
        raise HTTPException(status_code=404, detail="PPTX not found")
    # PDF가 없으면 변환
    if not pdf_path.exists():
        pptx_to_pdf(str(pptx_path.resolve()), str(pdf_path.resolve()))
    if not pdf_path.exists():
        raise HTTPException(status_code=500, detail="PDF 변환 실패")
    return FileResponse(pdf_path, media_type="application/pdf")


@app.get("/download/{ppt_id}")
async def download_ppt(ppt_id: str):
    ppt_path = UPLOAD_DIR / f"{ppt_id}.pptx"
    if not ppt_path.exists():
        raise HTTPException(status_code=404, detail="PPT not found")
    return FileResponse(ppt_path, media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation")


@app.post("/feedback", response_model=FeedbackResponse)
async def submit_feedback(feedback_data: FeedbackRequest):
    summary = await asyncio.to_thread(feedback.collect_feedback, feedback_data.responses)
    return FeedbackResponse(summary=summary, status="success")


@app.get("/")
async def root():
    """API 상태 확인"""
    return {
        "name": "EduFlow API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """헬스 체크"""
    return {"status": "healthy"}

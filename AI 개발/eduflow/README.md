# EduFlow - 학교 맞춤형 AI 발표자료 자동화 플랫폼

EduFlow는 학교 발표/과제 자동화, PPT/PDF 생성, 피드백 수집을 지원하는 멀티에이전트 기반 AI 플랫폼입니다.

## 주요 기능
- 텍스트 업로드 → PPT/PDF 자동 생성
- 학생 피드백 수집 및 요약
- 웹 UI 및 API 제공 (FastAPI)

## 폴더 구조
```
├── app/
│   ├── agents/         # AI 에이전트 (analyzer, master, feedback, orchestrator)
│   ├── schemas/        # Pydantic 스키마
│   ├── services/       # 외부 API/클라이언트
│   └── main.py         # FastAPI 진입점
├── templates/          # 사용자용 HTML 웹페이지
├── uploads/            # 업로드/생성된 파일 저장
├── requirements.txt    # Python 패키지 목록
├── Dockerfile          # 도커 배포 파일
```

## 실행 방법
1. 의존성 설치
   ```bash
   pip install -r requirements.txt
   ```
2. 서버 실행
   ```bash
   uvicorn app.main:app --reload
   ```
3. 웹사이트 접속
   - http://127.0.0.1:8000/ (사용자용 웹 UI)
   - http://127.0.0.1:8000/docs (API 문서)

## 배포/운영
- PowerPoint가 설치된 Windows 환경에서 PDF 변환 지원
- Dockerfile 포함 (단, PDF 변환은 Windows+PowerPoint 필요)

## 기여/문의
- Pull Request/이슈 환영!

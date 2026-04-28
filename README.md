# ppt-AI (EduFlow)
<img width="500" height="500" alt="image" src="https://github.com/user-attachments/assets/9f49654d-1fb4-4da0-9615-37be319f6940" />

학습 자료를 업로드하면 자동으로 PPT가 완성되는 AI 플랫폼입니다.  
멀티 에이전트 아키텍처로 문서를 분석하고, 슬라이드 구조를 생성한 뒤, `.pptx` 파일로 자동 출력합니다.

## 주요 기능

- 학습 자료(텍스트) 업로드 → PPT 자동 생성
- GPT-4o 기반 문서 요약 및 슬라이드 구조 생성
- 멀티 에이전트 아키텍처 (Orchestrator / Analyzer / Master / Feedback)
- `.pptx` 다운로드 및 PDF 변환 (Windows + PowerPoint 환경)
- 학생 피드백 수집 및 AI 분석 요약
- FastAPI 기반 REST API + Swagger UI (`/docs`)

## 기술 스택

**Backend**
- FastAPI
- Uvicorn
- LangChain + OpenAI (GPT-4o)
- python-pptx
- Pydantic
- Redis

## 폴더 구조

```
ppt-AI/
└── AI 개발/
    └── eduflow/
        ├── app/
        │   ├── agents/
        │   │   ├── analyzer.py       # 문서 분석 및 슬라이드 구조 생성
        │   │   ├── master.py         # PPT 슬라이드 생성
        │   │   ├── feedback.py       # 학생 피드백 수집 및 분석
        │   │   └── orchestrator.py   # 멀티 에이전트 워크플로우 조정
        │   ├── schemas/
        │   │   ├── presentation.py   # PPT 관련 Pydantic 스키마
        │   │   └── upload.py         # 업로드 관련 Pydantic 스키마
        │   ├── services/
        │   │   └── openai_client.py  # LangChain LLM 클라이언트
        │   └── main.py               # FastAPI 엔드포인트
        ├── Dockerfile
        └── requirements.txt
```

## 사전 준비

- Python 3.11 이상
- OpenAI API 키
- PDF 변환 기능 사용 시: Windows + Microsoft PowerPoint 설치 필요

## 설치 및 실행

**1. 의존성 설치**

```bash
cd "AI 개발/eduflow"
pip install -r requirements.txt
```

**2. 환경변수 설정**

`OPENAI_API_KEY` 환경변수를 설정합니다.

```bash
# Windows
set OPENAI_API_KEY=your-api-key

# Linux / macOS
export OPENAI_API_KEY=your-api-key
```

> API 키가 없어도 더미 모드로 실행은 가능합니다. (LLM 기능 비활성화)

**3. 서버 실행**

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

**4. API 문서 확인**

```
http://127.0.0.1:8000/docs
```

## API

| 메서드 | 경로 | 설명 |
|--------|------|------|
| `GET` | `/` | API 상태 확인 |
| `GET` | `/health` | 헬스 체크 |
| `POST` | `/upload` | 파일 업로드 → PPT 자동 생성 |
| `GET` | `/download/{ppt_id}` | 생성된 `.pptx` 파일 다운로드 |
| `GET` | `/download_pdf/{ppt_id}` | `.pptx` → PDF 변환 후 다운로드 |
| `POST` | `/feedback` | 학생 피드백 제출 및 AI 요약 |

### POST /upload

파일과 발표 대본을 업로드하면 PPT를 자동 생성합니다.

```
Content-Type: multipart/form-data

file   : 학습 자료 텍스트 파일
script : 발표 대본 또는 설명 텍스트
```

응답 예시:

```json
{
  "outline": "1. 서론\n2. 본론\n3. 결론",
  "script": "[요약] 핵심 내용...",
  "ppt_path": "uploads/xxxx.pptx",
  "status": "success"
}
```

### POST /feedback

학생 피드백 목록을 제출하면 AI가 요약 및 개선점을 반환합니다.

```json
{
  "responses": ["발표가 이해하기 쉬웠어요", "시각 자료가 더 있으면 좋겠어요"]
}
```

## 에이전트 구조

```
사용자 요청
    │
    ▼
Orchestrator  ← 전체 워크플로우 조정
    ├── Analyzer   : 문서 요약 + 슬라이드 구조(아웃라인) 생성
    ├── Master     : 아웃라인 → .pptx 파일 생성
    └── Feedback   : 학생 피드백 수집 및 AI 분석
```

## 자주 나는 문제

**PPT가 생성되지 않을 때**  
`OPENAI_API_KEY`가 설정되지 않으면 LLM 기능이 비활성화되어 더미 데이터로 PPT가 생성됩니다. API 키를 확인하세요.

**PDF 변환 실패**  
PDF 변환은 Windows 환경에서 Microsoft PowerPoint가 설치된 경우에만 동작합니다.  
`comtypes` 관련 오류가 발생하면 PowerPoint 설치 여부를 확인하세요.

**포트 충돌**  
8000 포트가 이미 사용 중이면 다른 포트로 실행하세요.

```bash
uvicorn app.main:app --reload --port 8001
```

# FAST API SERVER

## 1. 가상환경 생성

python -m venv .venv

## 2. 가상환경 활성화 (Ubuntu/macOS)

source .venv/bin/activate

## 3. 패키지 설치

python -m pip install -r requirements.txt

## 4. FastAPI 실행

python -m uvicorn app.main:app --reload --port 8001

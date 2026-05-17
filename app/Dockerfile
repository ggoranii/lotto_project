FROM python:3.11-slim

# 환경 변수 설정 (Python 출력 버퍼링 비활성화)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 작업 디렉토리 설정
WORKDIR /code

# 시스템 패키지 설치 (PostgreSQL 클라이언트)
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Python 패키지 설치 (캐시 활용을 위해 requirements.txt 먼저 복사!)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 소스 코드 복사
COPY . .

# entrypoint 스크립트 실행 권한 부여
RUN chmod +x entrypoint.sh

# 컨테이너 시작 시 실행할 스크립트
ENTRYPOINT ["./entrypoint.sh"]
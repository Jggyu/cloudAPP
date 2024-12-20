FROM ubuntu:22.04

# 환경 변수 설정
ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND noninteractive

# 시스템 패키지 설치
RUN apt-get update && apt-get install -y \
    python3.12.5 \
    python3-pip \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 작업 디렉토리 생성
WORKDIR /app

# 의존성 파일 복사 및 설치
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# 프로젝트 파일 복사
COPY . .

# gunicorn 설치 (프로덕션 서버)
RUN pip3 install gunicorn

# 포트 설정
EXPOSE 8000

# 실행 명령어
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "cloudAPP"]
FROM public.ecr.aws/amazonlinux/amazonlinux:2

WORKDIR /app

# 시스템 패키지 설치
RUN yum update -y && \
    yum install -y python3-devel python3-pip mysql-devel gcc && \
    yum clean all

# Python 가상환경 설정
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# requirements.txt 복사 및 설치
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY . .

# 포트 설정
EXPOSE 8000

# 실행 명령
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
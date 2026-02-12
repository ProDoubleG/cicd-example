# [1단계: 공통 기초 공사]
# 파이썬 깔고, 앱에 필요한 라이브러리 설치하는 단계
FROM python:3.9-slim as base
WORKDIR /app

# (중요) 빌드 위치가 루트(root)로 바뀔 예정이라 경로에 app/을 붙여야 함
COPY app/requirements.txt .
RUN pip install -r requirements.txt

# 앱 소스 코드 복사 (공통)
COPY app/ .

# ---------------------------------------------------

# [2단계: 테스트용 이미지] 
# 여기서는 테스트용 라이브러리를 더 깔고, tests 폴더를 복사함
FROM base as test-image
# 테스트용 라이브러리 추가 설치
RUN pip install pytest requests
# (중요) 루트에 있는 tests 폴더를 컨테이너 안으로 복사
COPY tests/ /tests
# 실행 명령어를 테스트 실행으로 변경
CMD ["pytest", "-v", "/tests/ci_test.py"]

# ---------------------------------------------------

# [3단계: 배포용 이미지 (최종)]
# 테스트 코드는 빼고, 순수하게 앱만 실행하는 단계
FROM base as production
WORKDIR /app
CMD ["python", "main.py"]
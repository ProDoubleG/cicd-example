FROM python:3.9-slim as base
WORKDIR /app

COPY app/requirements.txt .
RUN pip install -r requirements.txt

COPY app/ .

# IMAGE for my-app:tester
# The app from this image(app-tester) will run ci_test.py on app:test through docker network
FROM base as test-image

RUN pip install pytest requests

COPY tests/ /tests

CMD ["pytest", "-v", "/tests/ci_test.py"]

# ---------------------------------------------------

# IMAGE for my-app:prod
# The app from this image will be hosted on hostmachine
FROM base as production

WORKDIR /app
CMD ["python", "main.py"]
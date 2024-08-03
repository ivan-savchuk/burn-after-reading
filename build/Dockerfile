FROM python:3.12-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    curl \
    && pip3 install --no-cache-dir --upgrade pip

COPY ../requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
#RUN pip3 install --ignore-installed uvicorn==0.30.3

FROM python:3.12-slim AS runtime

WORKDIR /app/src
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY ../src/ src/
COPY ../data/ data/

EXPOSE 8000
CMD python3 -m uvicorn main:app --host 0.0.0.0 --port 8000
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    TZ=UTC

WORKDIR /work

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl make git tzdata ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /work/requirements.txt
RUN pip install --no-cache-dir -r /work/requirements.txt

COPY . /work

CMD ["bash", "scripts/run_all.sh"]

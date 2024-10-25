FROM python:3.12-slim-bookworm

WORKDIR /app

EXPOSE 8000

RUN apt-get update && \
    apt-get upgrade -y --no-install-recommends && \
    apt-get install -y --no-install-recommends curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install uv

COPY requirements.lock .
RUN pip install --no-cache-dir -r requirements.lock

COPY . .

SHELL ["/bin/bash", "-c"]
CMD ["python", "entry.py"]

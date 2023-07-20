# dev stage
FROM python:3.11-slim AS build-stage

RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    curl \
    apt-utils \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY app/ .

# prod stage
FROM python:3.11-slim AS production-stage

WORKDIR /app
COPY --from=build-stage /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=build-stage /app /app
CMD ["python", "main.py"]

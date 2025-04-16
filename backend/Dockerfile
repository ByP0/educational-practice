FROM python:3.11-alpine AS base
RUN apk add --no-cache bash postgresql-client

FROM base AS dev
WORKDIR /backend

COPY ./ ./
RUN mkdir -p /backend/alembic/versions

RUN pip install --no-cache-dir -r /backend/requirements.txt
RUN pip install alembic

COPY ./run_fastapi.sh /backend/run_fastapi.sh
RUN sed -i 's/\r//' /backend/run_fastapi.sh
RUN chmod +x /backend/run_fastapi.sh

CMD ["bash", "/backend/run_fastapi.sh"]
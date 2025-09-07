FROM apache/airflow:3.0.6-python3.12

RUN pip install uv

USER root

COPY pyproject.toml .
ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright

RUN uv pip install -r pyproject.toml
RUN uv run -- python3 -m playwright install --with-deps chromium && chown -R airflow:0 /ms-playwright || true
RUN rm -rf pyproject.toml

USER airflow
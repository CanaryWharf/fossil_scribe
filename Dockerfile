FROM python:3.11-slim
WORKDIR /app
COPY backend/ /app

COPY frontend/dist/ /app/fossil_scribe/dist/

RUN pip install poetry
RUN poetry export --format requirements.txt --with-credentials --output deploy_req.txt
RUN pip uninstall -y poetry
RUN pip install -r deploy_req.txt
EXPOSE 8080
CMD ["uvicorn", "fossil_scribe.endpoints:app", "--host", "0.0.0.0", "--port", "8080"]

FROM python:3.11-slim


WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

EXPOSE 8501
CMD ["uvicorn", "backend.api:app", "--port", "8000", "--host","0.0.0.0"]
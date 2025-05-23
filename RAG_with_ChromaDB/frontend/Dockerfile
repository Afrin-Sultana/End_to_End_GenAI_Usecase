FROM python:3.11-slim
WORKDIR /app
COPY ./frontend /app
COPY .env /app/.env
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir streamlit requests python-dotenv

EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
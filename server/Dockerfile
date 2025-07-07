from python:3.11-slim
WORKDIR /app
RUN pip install fastapi uvicorn docker python-dotenv
COPY . .
EXPOSE 9000
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "9000"]
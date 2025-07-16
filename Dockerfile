FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY /src/ /app/

WORKDIR /app/src/

CMD ["streamlit", "run", "main.py", "--server.address=0.0.0.0", "--server.port=8501"]

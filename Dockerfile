FROM python:3.11-slim

WORKDIR /app

RUN pip install uv

COPY requirements.txt .
RUN uv pip install --system -r requirements.txt

COPY . .

RUN python -c "from data.seed import seed_products; seed_products()"
RUN python -c "from data.ingest import ingest_products; ingest_products()"

EXPOSE 8501

CMD ["streamlit", "run", "app/main.py", "--server.port=8501", "--server.address=0.0.0.0"]
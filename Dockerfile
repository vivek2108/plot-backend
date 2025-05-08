FROM python:3.10

WORKDIR /app

COPY . /app

# RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -r requirements.txt

CMD ["sh", "-c", "python -m app.config.init_db && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"]

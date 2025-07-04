FROM python:3.11

WORKDIR /app
COPY . .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    playwright install

CMD ["python", "main.py"]

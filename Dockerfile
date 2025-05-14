FROM python:3.12-slim

# чтобы pip не кешировал *.whl
ENV PIP_NO_CACHE_DIR=1

WORKDIR /app

# 1) копируем только список зависимостей и ставим
COPY app/requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# 2) копируем весь код
COPY . /app

# 3) запуск uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
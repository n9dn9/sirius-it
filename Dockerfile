FROM python:3.12

WORKDIR /app

RUN pip install poetry

COPY . .
RUN poetry config virtualenvs.create false \
 && poetry install --no-root

COPY . .

RUN mkdir -p static/uploads

CMD ["gunicorn", "--preload"]
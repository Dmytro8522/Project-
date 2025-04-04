FROM python:3.11-slim
ENV PYTHONUNBUFFERED True
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
RUN mkdir -p uploads
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
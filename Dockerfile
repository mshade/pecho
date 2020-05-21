FROM python:3.8-alpine

WORKDIR /app

COPY src/requirements.txt /app

RUN pip install -U --no-cache pip && \
  pip install --no-cache -r requirements.txt

COPY src/ /app/

USER 1000

EXPOSE 8080
CMD gunicorn -w 4 -b 0.0.0.0:8080 --access-logfile - app:app

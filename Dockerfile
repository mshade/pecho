FROM alpine
LABEL maintainer="mshade@mshade.org"

RUN apk add --no-cache python3

WORKDIR /app
COPY src/requirements.txt /app

RUN pip3 install -U --no-cache pip && \
  pip3 install --no-cache -r requirements.txt

COPY src/ /app/
USER 1000
EXPOSE 8080
CMD gunicorn -w 4 -b 0.0.0.0:8080 --access-logfile - app:app


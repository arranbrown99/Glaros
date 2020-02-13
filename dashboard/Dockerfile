# BUILDER #
FROM python:3.8.0-alpine as builder

WORKDIR /usr/src/dashboard

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/dashboard/wheels -r requirements.txt

# FINAL #
FROM python:3.8.0-alpine

RUN mkdir -p /home/dashboard
RUN addgroup -S dashboard && adduser -S dashboard -G dashboard

ENV HOME=/home/dashboard
ENV APP_HOME=/home/dashboard/web
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/staticfiles
WORKDIR $APP_HOME

RUN apk update && apk add libpq
COPY --from=builder /usr/src/dashboard/wheels /wheels
COPY --from=builder /usr/src/dashboard/requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache /wheels/*

COPY ./entrypoint.prod.sh $APP_HOME
COPY . $APP_HOME
RUN chown -R dashboard:dashboard $APP_HOME

USER dashboard
# BUILDER #
FROM python:3.8.0-alpine as builder

WORKDIR $(HOME)/cs27-main/dashboard

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/dashboard/wheels -r requirements.txt

# FINAL #
FROM python:3.8.0-alpine

RUN addgroup -S dashboard && adduser -S dashboard -G dashboard

ENV HOME=$(HOME)/cs27-main
ENV APP_HOME=$(HOME)/cs27-main/dashboard
WORKDIR $APP_HOME

RUN apk update && apk add libpq
COPY --from=builder /usr/src/dashboard/wheels /wheels
COPY --from=builder /usr/src/dashboard/requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache /wheels/*

# COPY ./entrypoint.prod.sh $APP_HOME
# COPY . $APP_HOME
RUN chown -R dashboard:dashboard $APP_HOME

# USER dashboard
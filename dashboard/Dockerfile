# BUILDER #
FROM python:3.8.0-alpine as builder

WORKDIR /usr/src/dashboard

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/dashboard/wheels -r requirements.txt

# FINAL #
FROM python:3.8.0-alpine


# create directory for the dashbaord user
RUN mkdir -p /home/dashboard

# create the app user
RUN addgroup -S dashboard && adduser -S dashboard -G dashboard

# create the appropriate directories
ENV HOME=/home/dashboard
ENV APP_HOME=/home/dashboard/web
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/staticfiles
WORKDIR $APP_HOME

# install dependencies
RUN apk update && apk add libpq
COPY --from=builder /usr/src/dashboard/wheels /wheels
COPY --from=builder /usr/src/dashboard/requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache /wheels/*

# copy project
COPY . $APP_HOME

# chown all the files to the app user
RUN chown -R dashboard:dashboard $APP_HOME

# change to the app user
USER dashboard

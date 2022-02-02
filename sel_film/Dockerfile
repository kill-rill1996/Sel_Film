FROM python:3.9

#RUN mkdir -p /usr/src/app/

WORKDIR /usr/src/app

# buffer
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

COPY ./requirements.txt /usr/src/app

RUN pip install -r requirements.txt

COPY . /usr/src/app
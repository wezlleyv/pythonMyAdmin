FROM python
ENV PYTHONNUNBUFFERED 1

RUN mkdir -p /opt/flask
WORKDIR /opt/flask
ADD . /opt/flask

EXPOSE 5000

RUN pip install -r ./requirements.txt
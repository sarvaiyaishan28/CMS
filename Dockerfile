FROM python:3.8
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
RUN mkdir /static
RUN pip install --upgrade pip
ADD requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt
ADD . ./
RUN chmod +x ./docker-entrypoint.sh
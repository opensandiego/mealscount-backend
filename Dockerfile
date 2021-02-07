FROM python:3.7 AS base
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY *requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
RUN ./generate_state_json.sh
CMD python /code/server.py --host=0.0.0.0

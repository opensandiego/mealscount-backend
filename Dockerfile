FROM python:3.7 AS base
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY *requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
RUN python generate_state_json.py
CMD python /code/server.py --host=0.0.0.0

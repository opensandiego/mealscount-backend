FROM python:3.7 AS base
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY *requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/

FROM base AS release
RUN for d in `ls data`; do python cep_estimatory.py data/$d/latest.csv --output-folder dist/static/$d/; done;

CMD python /code/server.py --host=0.0.0.0

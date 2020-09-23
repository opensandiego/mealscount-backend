FROM python:3.7 AS base
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY *requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/

FROM node AS npm_build
COPY --from=base /code/ ./code
WORKDIR /code/
RUN npm install node-sass
RUN npm install .
RUN npm run build

FROM base AS release
COPY --from=npm_build /code/dist/ /code/dist
RUN python cep_estimatory.py data/ca/latest.csv --output-folder dist/static/ca/

CMD python /code/server.py --host=0.0.0.0

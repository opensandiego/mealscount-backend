FROM python:3.7 AS base
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY *requirements.txt /code/
RUN pip install -r requirements.txt
RUN pip install -r jupyter_requirements.txt
COPY . /code/
RUN python generate_state_json.py
CMD python /code/server.py --host=0.0.0.0

FROM node:14 AS npm_build
COPY --from=base /code/ ./code
WORKDIR /code/
RUN npm install node-sass
RUN npm install .
RUN npm run build

FROM base AS release
COPY --from=npm_build /code/dist/ /code/dist/

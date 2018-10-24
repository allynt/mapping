FROM python:3.6

LABEL maintainer "Allyn Treshansky"
LABEL project "mapping"

ENV APP_DIR=/opt/deployments/mapping

WORKDIR $APP_DIR

COPY . $APP_DIR

RUN apt update && apt install && apt install -y git build-essential libsqlite3-dev zlib1g-dev
RUN git clone https://github.com/mapbox/tippecanoe.git
RUN cd tippecanoe && make -j && make install
RUN pip install pipenv && pipenv install --system

EXPOSE 5000

CMD ["python", "app.py"]
FROM python:3.8 AS python-build
RUN pip install mysqlclient
RUN mkdir /app
WORKDIR /app
COPY requirements_base.txt /app/requirements_base.txt
RUN pip install --no-cache-dir -r requirements_base.txt

FROM python:3.8-slim-bullseye
RUN mkdir /app

WORKDIR /app
ENV TZ=America/Argentina/Buenos_Aires
COPY --from=python-build /usr/local/lib/python3.8/site-packages /usr/local/lib/python3.8/site-packages
COPY requirements.txt /app/requirements.txt

#RUN apt-get update
#RUN apt-get install -y libcairo2-dev
#RUN apt-get install -y libsdl-pango-dev
#RUN apt-get update && apt-get install -y --no-install-recommends \
   #libmariadb-dev-compat gcc                   `: MySQL client` \
#&& rm -rf /var/lib/apt/lists/*i
#RUN apt-get install -y default-libmysqlclient-dev
#COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt


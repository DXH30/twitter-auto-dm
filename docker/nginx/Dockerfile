FROM nginx:latest

RUN apt-get update

RUN apt-get install -y --no-install-recommends \
    libatlas-base-dev gfortran nginx supervisor python3-dev python3-pip

RUN python3 -m pip install uwsgi

RUN rm /etc/nginx/conf.d/default.conf

COPY docker/nginx/nginx.conf /etc/nginx/
COPY docker/nginx/flask-site-nginx.conf /etc/nginx/conf.d/
COPY docker/nginx/supervisord.conf /etc/

CMD ["/usr/bin/supervisord"]

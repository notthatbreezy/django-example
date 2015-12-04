FROM python:2.7-slim

MAINTAINER Azavea

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gdal-bin \
    libpq-dev \
    python-dev \
    git \
    postgresql-client-9.4 && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt
RUN pip install --no-cache-dir django-extensions

COPY opt/ /opt/

WORKDIR /opt/django_example

EXPOSE 8080

ENTRYPOINT ["gunicorn"]

CMD ["-w", "3", \
     "-b", "0.0.0.0:8080", \
     "--reload", \
     "--log-level", "info", \
     "--access-logfile", "-", \
     "--error-logfile", "-", \
     "-k", "gevent", \
     "django_example.wsgi"]

FROM python:3.9.7-slim-buster

RUN apt-get update && apt-get install -y \
  postgresql-server-dev-all \
  supervisor \
  python3-pip \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

ENV TZ=America/Argentina/Buenos_Aires
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

ENV PIP_DEFAULT_TIMEOUT=3600
ENV PIP_USE_MIRRORS=true
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

RUN mkdir /src
COPY qr /src

# COPY docker/pip.conf /etc/
# COPY docker/entrypoint.sh /
# COPY docker/supervisor/rest.conf /etc/supervisor/conf.d
# RUN cd /src && pip3 install --trusted-host pypi.econo.unlp.edu.ar --upgrade -e .

WORKDIR /src
RUN pip install -r requirements.txt

# ENTRYPOINT ["/entrypoint.sh"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
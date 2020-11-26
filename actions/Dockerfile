######################################################################
#  This Dockerfile is used for local development                     #
######################################################################

# RASA_SDK_IMAGE is passed from docker-compose.yml
ARG RASA_SDK_IMAGE
FROM ${RASA_SDK_IMAGE}

# Change back to root user to install dependencies
USER root

RUN apt-get update -qq \
 && apt-get install -y --no-install-recommends \
    # required by psycopg2 at build and runtime
    libpq-dev \
     # required for health check
    curl \
 && apt-get autoremove -y

#FROM base as builder

RUN apt-get update -qq && \
  apt-get install -y --no-install-recommends \
  build-essential \
  wget \
  openssh-client \
  graphviz-dev \
  pkg-config \
  git-core \
  openssl \
  libssl-dev \
  libffi6 \
  libffi-dev \
  libpng-dev

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/
WORKDIR /app

# Switch back to non-root to run code
#USER 1001
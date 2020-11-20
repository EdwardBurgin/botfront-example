######################################################################
#  This Dockerfile is used build your Rasa image                     #
######################################################################

# RASA_IMAGE is passed from docker-compose.yml which is generated
# from ./botfront/docker-compose-template.yml and ./botfront/botfront.yml

ARG RASA_IMAGE
FROM ${RASA_IMAGE}

# Change back to root user to install dependencies
USER root

COPY ./extensions/nlu/registry.py /opt/venv/lib/python3.7/site-packages/rasa/nlu/
COPY ./extensions/nlu/extractors/custom_spacy_entity_extractor_remote.py /opt/venv/lib/python3.7/site-packages/rasa/nlu/extractors/
COPY ./extensions/nlu/classifiers/ed_classifier.py /opt/venv/lib/python3.7/site-packages/rasa/nlu/classifiers

RUN python -m spacy download en_core_web_md
RUN python -m spacy link en_core_web_md en

# Switch back to non-root to run code
#USER 1001

# change shell
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# the entry point
EXPOSE 5005

ARG FLASK_SERVER_PORT
ARG FLASK_SERVER_IP

ENV flask_server_ip=${FLASK_SERVER_IP}
ENV flask_server_port=${FLASK_SERVER_PORT}

# EXPOSE ${FLASK_SERVER_PORT}

ENTRYPOINT ["rasa"]
CMD ["run", "--enable-api", "--debug"]

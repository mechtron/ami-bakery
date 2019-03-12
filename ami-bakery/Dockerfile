FROM ubuntu:16.04
LABEL maintainer "GumGum Ops <ops@gugum.com>"

ARG PACKER_VERSION
ENV PACKER_VERSION ${PACKER_VERSION:-1.3.2}

# General system deps and Ansible
RUN apt-get update \
    && apt-get install -y \
      wget unzip \
      software-properties-common \
      python3-dev python3-pip libssl-dev libffi-dev \
    && pip3 install --upgrade pip boto3

# Packer install
RUN wget -q -P /tmp https://releases.hashicorp.com/packer/${PACKER_VERSION}/packer_${PACKER_VERSION}_linux_amd64.zip \
    && unzip -d /usr/bin/ /tmp/packer_${PACKER_VERSION}_linux_amd64.zip \
    && rm /tmp/packer_${PACKER_VERSION}_linux_amd64.zip

RUN mkdir /opt/bakery
ADD *.py /opt/bakery/
RUN ln -s /opt/bakery/bakery.py /usr/bin/bake

CMD ["bake"]

FROM python:3.7.2

WORKDIR /usr/local/app
ADD Pipfile.lock .
RUN pip install pipenv==2018.11.26 && \
    pipenv install --ignore-pipfile -d

# install fixuid
# copy source from https://boxboat.com/2017/07/25/fixuid-change-docker-container-uid-gid/
ENV FIXUID_VERSION=0.4
RUN addgroup --gid 1000 docker && \
    adduser --uid 1000 --ingroup docker --home /home/docker --shell /bin/sh --disabled-password --gecos "" docker
RUN USER=docker && \
    GROUP=docker && \
    curl -SsL https://github.com/boxboat/fixuid/releases/download/v${FIXUID_VERSION}/fixuid-${FIXUID_VERSION}-linux-amd64.tar.gz | tar -C /usr/local/bin -xzf - && \
    chown root:root /usr/local/bin/fixuid && \
    chmod 4755 /usr/local/bin/fixuid && \
    mkdir -p /etc/fixuid && \
    printf "user: $USER\ngroup: $GROUP\n" > /etc/fixuid/config.yml
USER docker:docker
ENTRYPOINT ["fixuid", "-q"]
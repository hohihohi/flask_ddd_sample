FROM python:3.7.2

WORKDIR /usr/local/app
ADD Pipfile.lock .
RUN pip install pipenv==11.10.4 && \
    pipenv install --ignore-pipfile -d

ENTRYPOINT ["pipenv", "run"]

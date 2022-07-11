FROM python:3.8.3-slim-buster

RUN useradd deploy_script

WORKDIR /home/deploy_script

RUN pip install pipenv

COPY . ./

RUN pipenv install --system --deploy

RUN pip install pytest

RUN pytest test_functions.py

CMD ["python","./main.py"]
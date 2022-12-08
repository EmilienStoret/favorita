FROM python:3.10.8-buster
WORKDIR /prod
COPY favorita favorita
COPY requirements_prod.txt requirements.txt
COPY setup.py setup.py
RUN pip install .
CMD uvicorn favorita.API.fast_api:app --host 0.0.0.0 --port $PORT

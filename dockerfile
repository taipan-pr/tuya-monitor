FROM python:alpine3.16

WORKDIR /src

COPY ./src .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]

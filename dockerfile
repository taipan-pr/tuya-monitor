FROM python:3.10

WORKDIR /code

COPY ./src .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "./main.py"]
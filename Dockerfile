FROM python:3.8.12

EXPOSE 8000

RUN apt-get update
COPY requirements.txt .
RUN pip install -r requirements.txt 

WORKDIR /app
COPY . /app 

CMD ["uvicorn", "api_image:app", "--reload", "--host", "0.0.0.0"]

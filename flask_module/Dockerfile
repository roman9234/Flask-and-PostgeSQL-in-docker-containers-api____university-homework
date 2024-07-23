FROM python:3.9

COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
RUN apt update
RUN apt install iputils-ping -y
EXPOSE 5000
#CMD ["python", "app.py"]
#CMD ["flask", "run", "--host", "0.0.0.0"]

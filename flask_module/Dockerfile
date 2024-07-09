FROM python:3

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 6000
CMD ["python", "flask_server.py"]
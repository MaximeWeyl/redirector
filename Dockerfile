FROM python:3.9-alpine3.15
WORKDIR /root/project/

# Using a requirements.txt keeps a smaller image size than embedding poetry
# you can create this file with 'poetry export'
COPY requirements.txt ./requirements.txt

RUN pip install -r requirements.txt
COPY main.py /root/project/src/main.py
CMD ["python", "src/main.py"]

EXPOSE 8080

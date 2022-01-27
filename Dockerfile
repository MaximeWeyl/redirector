FROM python:3.9-alpine3.15
WORKDIR /project/

# Using a requirements.txt keeps a smaller image size than embedding poetry
# you can create this file with 'poetry export'
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
COPY main.py ./src/main.py
CMD ["python", "src/main.py"]

# So the image can be used with any non root user, which can be usefull for usage in
# OVHcloud AI-Training for instance.
RUN chmod -R a+rx /project

EXPOSE 8080

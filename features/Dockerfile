FROM python:3.9
WORKDIR /usr/src/app
COPY ./src /usr/src/app/src
COPY ./requirements.txt /usr/src/app
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "src/features.py"]

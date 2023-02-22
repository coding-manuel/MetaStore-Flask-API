# FROM python:3.8-slim-buster
# COPY . /app
# WORKDIR /app
# RUN apt-get update
# RUN pip3 install -r requirements.txt
# EXPOSE 5000
# ENTRYPOINT [ "python" ]
# CMD [ "application.py" ]
FROM tensorflow/tensorflow

RUN apt-get update && apt-get install -y git-lfs
RUN git clone https://github.com/coding-manuel/MetaStore-Flask-API.git
RUN git lfs fetch && git lfs checkout

# Copy local code to the container image.
COPY . /app
WORKDIR /app

# Install production dependencies.
RUN pip3 install -r requirements.txt

ENV PORT 5000
EXPOSE 5000

ENTRYPOINT [ "python" ]
CMD [ "application.py" ]

# webserver, with one worker process and 8 threads.
# CMD exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 8 --timeout 0 main:app
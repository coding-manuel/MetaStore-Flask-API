FROM tensorflow/tensorflow
COPY . /app
WORKDIR /app
RUN apt-get update
RUN pip3 install -r requirements.txt
EXPOSE 5000
ENTRYPOINT [ "python" ]
CMD [ "application.py" ]
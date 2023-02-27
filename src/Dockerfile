FROM tensorflow/tensorflow:latest-py3
COPY . /app
WORKDIR /app
RUN apt-get update && apt-get install -y wget
RUN pip install -r requirements.txt
RUN wget -O model/model.h5 "https://www.dropbox.com/s/0dj5nk6nve8o939/model.h5?dl=1"
EXPOSE 5000
# CMD ["python", "application.py"]
CMD ["gunicorn", "-b", "0.0.0.0:5000", "application:app", "--workers=2"]
# gunicorn -b 0.0.0.0:5000 application:app --workers=2
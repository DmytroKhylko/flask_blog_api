FROM python:3.9-buster
RUN mkdir /usr/src/api/
RUN mkdir /usr/src/api/blog_api
ENV FLASK_APP=blog_api.create_app:create_app
COPY . /usr/src/api/
WORKDIR /usr/src/api
RUN pip install -r requirements.txt
RUN chmod +x ./wait-for-it.sh
CMD chmod +x ./init.sh && ./init.sh
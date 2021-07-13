FROM python:3.9-buster
RUN mkdir /usr/src/api/
RUN mkdir /usr/src/api/blog_api
ENV FLASK_APP=blog_api.create_app:create_app
COPY . /usr/src/api/
WORKDIR /usr/src/api
RUN pip install -r requirements.txt
CMD chmod +x ./init.sh && chmod +x ./wait-for-it.sh && ./wait-for-it.sh db:5432 -- ./init.sh
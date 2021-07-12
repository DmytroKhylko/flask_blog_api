FROM python:3.9-buster
RUN mkdir /usr/src/api/
RUN mkdir /usr/src/api/blog_api
ENV FLASK_APP=blog_api::__main__.py
COPY . /usr/src/api/
WORKDIR /usr/src/api
# RUN apk update && apk add --virtual build-deps gcc python3-dev musl-dev libffi-dev build-base && apk add postgresql-dev && apk add openssl-dev cargo
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["blog_api/__main__.py"]
# CMD [ "flask run" ]
FROM python:3.9-alpine
RUN mkdir /usr/src/api/
RUN mkdir /usr/src/api/blog_api
ENV FLASK_APP=api.py
COPY . /usr/src/app/
WORKDIR /usr/src/app/blog_api
RUN apk update && apk add --virtual build-deps gcc python3-dev musl-dev libffi-dev build-base && apk add postgresql-dev && apk add openssl-dev cargo
RUN pip install -r ../requirements.txt
ENTRYPOINT ["python"]
CMD ["api.py"]

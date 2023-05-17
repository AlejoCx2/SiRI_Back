FROM python:3.11.3-alpine3.18

WORKDIR /app

RUN  apk update \
	&& pip install --upgrade pip

COPY . .

RUN pip install -r requirements.txt

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]
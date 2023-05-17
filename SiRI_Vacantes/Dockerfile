FROM python:3.11.3-alpine3.18

WORKDIR /app

RUN  apk update \
	&& pip install --upgrade pip

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]
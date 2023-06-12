FROM python:3.10-alpine3.18

WORKDIR /app

RUN  apk update \
	&& pip install --upgrade pip

RUN apk update
RUN apk add make automake gcc g++ gfortran openblas-dev

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]
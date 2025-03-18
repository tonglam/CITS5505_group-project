FROM python:3.11-slim-bullseye

WORKDIR /home/workspace/askify

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt gunicorn

COPY . .

EXPOSE 5000

ENV FLASK_ENV=prod 

CMD ["gunicorn", "-b", "0.0.0.0:5000", "run:app"]
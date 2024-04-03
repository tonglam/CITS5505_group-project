FROM python:3.11-slim-bullseye

WORKDIR /var/www/cits5505_group-project

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
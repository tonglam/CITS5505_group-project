FROM python:3.11-slim-bullseye

WORKDIR /home/workspace/cits5505

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

ENV FLASK_ENV=prod 

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
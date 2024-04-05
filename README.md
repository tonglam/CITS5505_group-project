# CITS5505_group-project

This repository is dedicated to the CITS5505 group project, focused on building a request forum application.

## Get Started

1. Create a virtual environment (venv) for the project in VSCode:

   - Use the shortcut `Cmd + Shift + P` to access VSCode commands.
   - Select `> Python: Select Interpreter`.
   - Click on `Create Virtual Environment - Venv`.
   - Use the shortcut `Cmd + J` to open the terminal.
   - If the terminal command line starts with `(.venv)`, you're in the virtual environment.

2. Use `requirements.txt` to install the necessary libaries.

```python
pip install -r requirements.txt
```

3. Set up Environment: Use the `config.ini.example` as a template in `config_dev.ini` or `config_prod.ini`. Configure the development or production environment accordingly.

```python
# using command line
export FLASK_ENV=development # load config_dev.ini

export FLASK_ENV=production # load config_prod.ini
```

4. Start the Flask App. The app runs on http://127.0.0.1:5000.

```python
flask run
# or run in debug mode
flask run --debug
```

# Use Docker

1. Start the Docker daemon, such as `Docker Desktop`, on your local machine or server.

2. Execute the following command in the terminal.

```shell
# run docker container
docker compose up

# run docker container in background
docker compose up -d

# stop docer container
docker compose down
```

3. If you want to run the docker directly:

```shell
docker tag cits5505_group-project tonglam/cits5505_group-project:lastest

docker run -p 5000:5000 tonglam/cits5505_group-project:lastest

docker run -d -p 5000:5000 tonglam/cits5505_group-project:lastest
```

4. If you want to push a new image to Docker Hub:

```python
 docker tag cits5505_group-project tonglam/cits5505_group-project:lastest

 docker build --pull --rm -f "Dockerfile" -t cits5505_group-project:latest "."

 docker push tonglam/cits5505_group-project:lastest
```

# Run Test

All the tests in this project are located in the `test.py` file.

To run the tests, navigate to the root directory of the project and execute the `test.py` file.

```python
python test.py
```

# Deployment

The main branch is used for deploying to production. [Visit Here](https://letletme.cc)

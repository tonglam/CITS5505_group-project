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

3. Set up Environment: Use the `config.ini.example` as a template in `config_dev.ini` or `config_prod.ini`. Configure the dev or prod environment accordingly.

```python
# using command line
export FLASK_ENV=dev # load config.dev.ini

export FLASK_ENV=prod # load config.prod.ini
```

4. Start the Flask App. The app runs on http://127.0.0.1:5000.

```python
FLASK_ENV=dev flask run
# or run in debug mode
FLASK_ENV=dev flask run --debug
```

# Use Docker

1. Start the Docker daemon, such as `Docker Desktop`, on your local machine or server.

2. Execute the following command in the terminal.

```shell
# run docker container
docker-compose -f docker-compose.dev.yml up

# run docker container in background
docker-compose -f docker-compose.dev.yml up -d

# stop docer container
docker-compose -f docker-compose.dev.yml down
```

3. If you want to run the docker directly:

```shell
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

All the tests in this project are located in the `/tests/` directory, and file names start with `test_`.

To run the tests, navigate to the root directory of the project and execute the `test.py` file:

```python
python test.py
```

If you want to test a specific module, use the module name as the third argument:

```python
python test.py [api|auth|community|...]
```

# Deployment

The main branch is used for deploying to production. [Visit Here](https://letletme.cc)

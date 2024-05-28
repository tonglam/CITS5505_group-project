# Askify

This repository is dedicated to the CITS5505 group project, which developed a request forum called 'Askify'.

Askify enables users to create their own communities and posts with text and pictures, as well as reply to, like/unlike, save/unsave any post they choose.

Additionally, Askify allows users to manage their profiles, including changing their avatar, username, email, and password. Users can also track their activity on the platform, viewing the posts they have created, replied to, or saved.

Moreover, Askify provides a full-text search feature to find any community or post you are looking for. You can search using the title, content, or author to get the results you want.

Askify ensures your protection by offering industry-standard authentication mechanisms, and all APIs on the platform are secure. You don't need to worry about your data or privacy being compromised.

You can quickly access the platform using your Google or GitHub account, or you can register a new account to start enjoying Askify.

> ASKIFY, UNLOCKING KNOWLEDGE.

# Get Started

There are two ways to get started; you can choose either way you prefer.

## Clone the Repository

You can clone the repo and set it up by following these steps:

### Clone from Github

Use `https://github.com/tonglam/CITS5505_group-project.git` to clone the repo to your machine.

### Set Up Virtual Environment

Create a virtual environment (venv) for the project. Using `VSCode` as an example:

- Use the shortcut `Cmd + Shift + P` to access VSCode commands.
- Select `> Python: Select Interpreter`.
- Click on `Create Virtual Environment - Venv`.
- Use the shortcut `Cmd + J` to open the terminal.
- If the terminal command line starts with `(.venv)`, you're in the virtual environment.

### Install Requirements

Use `requirements.txt` to install the necessary libraries.

```shell
pip install -r requirements.txt
```

### Set Up Environment Config

Use the `config.ini.example` as a template to create a `config.dev.ini` file or `config.prod.ini` file, which will be used in the dev or prod environment accordingly.

If you only want to run it under `dev` environment, all you need is to create a `config.dev.ini` file under root directory.

#### `config.ini` Explanation:

Replace the following keys to start the Flask app with the minimum configuration.

```
[APP]
SECRET_KEY = example-key
JWT_SECRET_KEY = jwt-example-key

[SQLITE]
DATABASE_URL = sqlite:///example.dev.sqlite
```

- Replace the following keys using your own [Google OAuth token](https://console.cloud.google.com/apis/dashboard) and [Github OAuth token](https://github.com/settings/developers), to use Google/Github authentication.

```
[GOOGLE]
CLIENT_ID = example_id
CLIENT_SECRET = example_secret
CALLBACK_URL = http://127.0.0.1:5000/auth/callback/google

[GITHUB]
CLIENT_ID = example_id
CLIENT_SECRET = example_secret
CALLBACK_URL = http://127.0.0.1:5000/auth/callback/github
```

- Replace the following keys using your [ImageBB Api key](https://api.imgbb.com/) to use upload picture service.

```
[IMGBB]
API_KEY = example_key
```

```python
# using command line
export FLASK_ENV=dev # load config.dev.ini

export FLASK_ENV=prod # load config.prod.ini
```

### Start the Flask App

The app runs on http://127.0.0.1:5000. And the default env is `dev`.

```python
flask run
# or run in debug mode
flask run --debug
```

## Use Docker

A simpler way to enjoy Ask is to use our Docker image.

### Start the Docker daemon

Start the Docker daemon, such as `Docker Desktop`, on your local machine or server.

### Run and Stop the Docker

Execute the following command in the terminal.

```shell
# run docker container
docker-compose -f docker-compose.dev.yml up

# run docker container in background
docker-compose -f docker-compose.dev.yml up -d

# stop docer container
docker-compose -f docker-compose.dev.yml down
```

Alternatively, if you want to run Docker directly:

```shell
docker run -p 5000:5000 tonglam/cits5505_group-project:lastest

docker run -d -p 5000:5000 tonglam/cits5505_group-project:lastest
```

# Run Test

The Askify project has two kinds of tests: unit tests and end-to-end tests using Selenium. We provide an easy way to run these tests.

The `test.py` file is located in the root directory.

## Unit Test

To run all the unit tests, execute the following command in the terminal:

```python
python test.py
```

### Module Unit Test

If you want to run unit tests for a specific module, use the following command:

```python
python test.py [api|auth|community|popular|post|search|user]
```

## End to End Test

To run the Selenium end-to-end tests, execute the following command in the terminal:

```python
python test.py end2end
```

# Module

## Auth

The Auth module provides services for registering, logging in, and resetting forgotten passwords.

## Api

The Api module integrates all the APIs of Askify, and all endpoints are protected by JWT.

## Community

The Community module provides services for adding, editing, deleting, and viewing communities.

## Job

The Job module contains scheduled jobs.

## Notice

The Notice module uses the observer design pattern to implement a publish-subscribe mechanism for notifications.

## Popular

The Popular module provides services for displaying trending posts and communities.

## Post

The Post module provides services for adding, editing, deleting, and viewing posts and replies.

## Search

The Search module provides services for full-text search.

## User

The User module provides services for displaying, editing user profiles, and tracing user behaviors on the platform.

# Main Techniques

- **Flask** for creating the web server.
- **Jinja2** for rendering the templates.
- **SQLite** for database.
- **Bootstrap** for frontend UI.
- **JavaScript** and **jQuery** for DOM manipulation and Ajax.
- **Flask-Login** for user session management.
- **Flask-SQLAlchemy** and Flask-Migrate for SQLite database - management.
- **Flask-WTF** for form validation.
- **Flask-JWT-Extended** for implementing JWT for APIs.
- **flasgger** for creating Swagger documentation.
- **Flask-APScheduler** for implementing scheduled jobs.
- **flask-unittest** for integrating unit tests and selenium tests.

# Documentation

If you encounter any issues when using Askify, you can look into the [Wiki](https://github.com/tonglam/CITS5505_group-project/wiki) for this repo. It may contain useful information, as we maintain the documentation throughout the development process.

# Deployment

The main branch is used for deploying to production. [Visit Here](https://letletme.cc)

# Swagger

We also use Swagger (Flasgger) for API documentation in this project. [Visit Here](https://letletme.cc/apidocs/).

# Reference

- [ChatGPT](https://chatgpt.com/).
- [perplexity](https://www.perplexity.ai/).
- [Bootstrap](https://getbootstrap.com/docs/5.3/getting-started/introduction/).
- [Bootdey](https://www.bootdey.com/).
- [Freefrontend](https://freefrontend.com/).
- [fontawesome](https://fontawesome.com/icons).
- [miguelgrinberg](https://blog.miguelgrinberg.com/).
- [Flask](https://flask.palletsprojects.com/en/3.0.x/).
- [flask-bones](https://github.com/cburmeister/flask-bones).
- [flask-unittest](https://github.com/TotallyNotChase/flask-unittest).

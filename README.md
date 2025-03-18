# Askify

This repository is dedicated to the CITS5505 group project, which developed a request forum called 'Askify'.

Askify enables users to create their own communities and posts with text and pictures, as well as reply to, like/unlike, save/unsave any post they choose.

Additionally, Askify allows users to manage their profiles, including changing their avatar, username, email, and password. Users can also track their activity on the platform, viewing the posts they have created, replied to, or saved.

Moreover, Askify provides a full-text search feature to find any community or post you are looking for. You can search using the title, content, or author to get the results you want.

Askify ensures your protection by offering industry-standard authentication mechanisms, and all APIs on the platform are secure. You don't need to worry about your data or privacy being compromised.

You can quickly access the platform using your Google or GitHub account, or you can register a new account to start enjoying Askify.

> ASKIFY, UNLOCKING KNOWLEDGE.

## Tech Stack

- 🎯 **Backend**: Flask, Python, Jinja2
- 🗄️ **Database**: PostgreSQL (Production), SQLite (Testing), Flask-SQLAlchemy, Flask-Migrate
- 🔐 **Authentication**: Flask-Login, JWT (Flask-JWT-Extended), OAuth2 (Google/GitHub)
- 🎨 **Frontend**: Bootstrap 5, JavaScript, jQuery
- 🔍 **Search**: Full-text search with PostgreSQL
- 📦 **Storage**: Cloudflare R2
- 🚀 **Deployment**: Docker, Render
- 📝 **Documentation**: Swagger/Flasgger
- 🔄 **CI/CD**: GitHub Actions
- 🧪 **Testing**: flask-unittest (Unit & Selenium Tests)
- 🛠️ **Utils**: Flask-WTF (Form Validation), Flask-APScheduler (Scheduled Jobs)

## System Architecture

```mermaid
graph TD
    Client[Web Browser] -->|HTTP/HTTPS| Flask[Flask Application]
    Flask -->|Authentication| Auth[Auth Module]
    Auth -->|OAuth| OAuth[Google/GitHub OAuth]
    Auth -->|JWT| JWT[JWT Service]
    Flask -->|Data Access| DB[(PostgreSQL)]
    Flask -->|File Storage| R2[Cloudflare R2]
    Flask -->|Search| Search[Search Module]
    Flask -->|Community| Community[Community Module]
    Flask -->|Post| Post[Post Module]
    Flask -->|User| User[User Module]
    Search -->|Query| DB
    Community -->|CRUD| DB
    Post -->|CRUD| DB
    User -->|Profile| DB
    User -->|Avatar| R2
```

## Deployment Flow

```mermaid
graph LR
    Dev[Local Development] -->|Git Push| GitHub[GitHub Repository]
    GitHub -->|Auto Deploy| Render[Render Platform]
    Render -->|Build| Build[Build Process]
    Build -->|Deploy| Web[Web Service]
    Web -->|Serve| Users[End Users]
    Web -->|Connect| DB[(PostgreSQL DB)]
    Web -->|Store| R2[Cloudflare R2]
```

# Get Started

There are two ways to get started; you can choose either way you prefer.

## Clone the Repository

You can clone the repo and set it up by following these steps:

### Clone from Github

Use `https://github.com/tonglam/Askify.git` to clone the repo to your machine.

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

You can configure the application using either a `.ini` file or a `.env` file:

#### Option 1: Using `.ini` files (Traditional method)

Use the `config.ini.example` as a template to create a `config.dev.ini` file or `config.prod.ini` file, which will be used in the dev or prod environment accordingly.

If you only want to run it under `dev` environment, all you need is to create a `config.dev.ini` file under root directory.

#### Option 2: Using `.env` file (Alternative method)

Alternatively, you can create a `.env` file in the root directory. This is a common modern approach that's well-supported by many tools and hosting platforms.

Here's an example of the minimum required configuration in your `.env` file:

```shell
# Flask Application Settings
FLASK_ENV=development
APP_SECRET_KEY=your-secret-key
APP_JWT_SECRET_KEY=your-jwt-secret-key

# PostgreSQL Database
POSTGRESQL_DATABASE_URL=postgresql://username:password@localhost:5432/dbname

# OAuth Configuration (Optional)
GOOGLE_OAUTH_CLIENT_ID=your-google-client-id
GOOGLE_OAUTH_CLIENT_SECRET=your-google-client-secret
GOOGLE_OAUTH_REDIRECT_URI=http://127.0.0.1:5000/auth/callback/google

GITHUB_OAUTH_CLIENT_ID=your-github-client-id
GITHUB_OAUTH_CLIENT_SECRET=your-github-client-secret
GITHUB_OAUTH_REDIRECT_URI=http://127.0.0.1:5000/auth/callback/github

# Cloudflare Configuration (Optional)
CLOUDFLARE_ACCOUNT_ID=your-cloudflare-account-id
CLOUDFLARE_API_TOKEN=your-cloudflare-api-token
CLOUDFLARE_R2_BUCKET=your-r2-bucket-name
CLOUDFLARE_R2_PUBLIC_URL=your-r2-public-url
```

The application will automatically detect and use the `.env` file if present. If both `.ini` and `.env` files exist, the `.env` file takes precedence.

> Note: Make sure to add `.env` to your `.gitignore` file to prevent sensitive information from being committed to version control.

#### `config.ini` Explanation:

Replace the following keys to start the Flask app with the minimum configuration.

```
[APP]
SECRET_KEY = example-key
JWT_SECRET_KEY = jwt-example-key

[POSTGRESQL]
DATABASE_URL = postgresql://username:password@localhost:5432/dbname

[SQLITE]
DATABASE_URL = sqlite:///example.test.sqlite  # Used for unit tests
```

- Replace the following keys using your own [Google OAuth token](https://console.cloud.google.com/apis/dashboard) and [Github OAuth token](https://github.com/settings/developers), to use Google/Github authentication.

```
[GOOGLE]
GOOGLE_OAUTH_CLIENT_ID = your-google-client-id
GOOGLE_OAUTH_CLIENT_SECRET = your-google-client-secret
GOOGLE_OAUTH_REDIRECT_URI = http://127.0.0.1:5000/auth/callback/google
# The following URLs are constants, no need to change
GOOGLE_OAUTH_AUTH_URL = https://accounts.google.com/o/oauth2/v2/auth
GOOGLE_OAUTH_TOKEN_URL = https://oauth2.googleapis.com/token
GOOGLE_OAUTH_USER_INFO_URL = https://www.googleapis.com/oauth2/v3/userinfo
GOOGLE_OAUTH_SCOPE_PROFILE = https://www.googleapis.com/auth/userinfo.profile
GOOGLE_OAUTH_SCOPE_EMAIL = https://www.googleapis.com/auth/userinfo.email

[GITHUB]
GITHUB_OAUTH_CLIENT_ID = your-github-client-id
GITHUB_OAUTH_CLIENT_SECRET = your-github-client-secret
GITHUB_OAUTH_REDIRECT_URI = http://127.0.0.1:5000/auth/callback/github
# The following URLs are constants, no need to change
GITHUB_OAUTH_AUTH_URL = https://github.com/login/oauth/authorize
GITHUB_OAUTH_TOKEN_URL = https://github.com/login/oauth/access_token
GITHUB_OAUTH_USER_INFO_URL = https://api.github.com/user

[CLOUDFLARE]
ACCOUNT_ID = your-cloudflare-account-id
API_TOKEN = your-cloudflare-api-token
R2_BUCKET_NAME = your-r2-bucket-name
R2_PUBLIC_URL = your-r2-public-url

```

[IMGBB]
API_KEY = example_key

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

Start the Docker daemon, such as `Docker Desktop` or `Orbstack`, on your local machine or server.

### Run and Stop the Docker

Execute the following command in the terminal.

```shell
# run docker container
docker-compose -f docker-compose.dev.yml up

# run docker container in background
docker-compose -f docker-compose.dev.yml up -d

# stop docker container
docker-compose -f docker-compose.dev.yml down
```

Alternatively, if you want to run Docker directly:

```shell
# run docker container
docker run -p 5000:5000 docker.io/tonglam/askify:latest

# run docker container in background
docker run -d -p 5000:5000 docker.io/tonglam/askify:latest
```

Note: When running with Docker, make sure to set up the required environment variables. You can use the `-e` flag or create a `.env` file:

```shell
# Example of setting environment variables
docker run -p 5000:5000 \
  -e SECRET_KEY=your-secret-key \
  -e JWT_SECRET_KEY=your-jwt-secret \
  -e DATABASE_URL=your-database-url \
  -e GOOGLE_OAUTH_CLIENT_ID=your-google-client-id \
  ... (other environment variables) \
  docker.io/tonglam/askify:latest
```

# Run Test

The Askify project has two kinds of tests: unit tests and end-to-end tests using Selenium. We provide an easy way to run these tests.

The `test.py` file is located in the root directory.

## Unit Test

To run all the unit tests, execute the following command in the terminal. Note that unit tests use SQLite as the database for faster execution and easier setup:

```python
python test.py
```

### Module Unit Test

If you want to run unit tests for a specific module, use the following command:

```python
python test.py [api|auth|community|popular|post|search|user]
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

# Documentation

If you encounter any issues when using Askify, you can look into the [Wiki](https://github.com/tonglam/Askify/wiki) for this repo. It may contain useful information, as we maintain the documentation throughout the development process.

# Deployment

The main branch is deployed on [Render](https://render.com), a modern cloud platform that automatically builds and deploys web services from Git. [Visit Here](https://askify-q4k0.onrender.com)

> Note: The application is hosted on Render's free tier, which may cause the initial load to take a few seconds if the service has been inactive.

# Swagger

We also use Swagger (Flasgger) for API documentation in this project. [Visit Here](https://askify-q4k0.onrender.com/apidocs/).

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
- [Render Documentation](https://docs.render.com/).
- [Cloudflare R2 Documentation](https://developers.cloudflare.com/r2/).
- [Cloudflare API Documentation](https://api.cloudflare.com/).

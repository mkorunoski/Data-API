# Data API

Solution for the Swisscom's coding challenge for the Data Science position.

**Candidate**: Mladen Korunoski
**Date**: 08/08/2022

## Instalation

First, create a [Conda](https://www.anaconda.com/products/distribution) virtual environment and activate it.
```
conda create -n swisscom-ds-challenge
conda activate swisscom-ds-challenge
```
Then, install the Python package installer, **pip**:
```
conda install pip
```
Afterwards, install the necessary requirements:
```
pip install -r requirements.txt
```

### Redis

This solution uses Redis for caching. For this, we are going to run Redis in a [Docker](https://www.docker.com/) container.
```
docker run --name redis-cache -p 6379:6379 -d redis
```

## Test

In order to run the test, execute the following command in root:
```
pytest
```

## Run

The application stores the dialogs in SQLite database. In the root folder, create an instance of the database.
```
flask --app dialogs init-db
```
While still in the root folder, run the application.
```
flask --app dialogs --debug run
```
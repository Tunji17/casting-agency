# Backend API For Casting Agency App 

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, create a database and add an env variable 'DATABASE_URL' which is your postgres connection url,
run migrations using:
```bash
flask db init
flask db migrate
flask db upgrade
```

## Running the server

From within the your directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=src/app.py
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `src/app.py` directs flask to use the app.py` file to run the application.

## Endpoints
GET '/actors'
GET '/movies'
POST '/actors'
POST '/movies'
PATCH '/actors/<int:actor_id>'
PATCH '/movies/<int:movie_id>'
DELETE '/actors/<int:actor_id>'
DELETE '/movies/<int:movie_id>'

## Testing
To run the tests, run
```
python src/test_app.py
```

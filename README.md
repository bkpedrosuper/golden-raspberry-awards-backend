# golden-raspberry-awards-backend
API made with Python-Flask for Golden Raspberry Awards

## Initial Setup
After clone, you must create a `.env` file in the root of the project.
Example:
```
DEBUG=True
DB_PATH=app/db_files/movielist.csv
DB_TEST_PATH=app/db_files/movielist_test.csv
```

## Install dependencies

### With Poetry
This project is recommended to be loaded with Poetry.
```
poetry shell
poetry install
```

### With pip
You can also run this project with pip:
```
pip install -r requirements.txt
```

## Run project
After install dependencies, the project can be run with:
```
python main.py
```

## Tests
Tests can be run with:
```
pytest
```

## Tryout!
Once the application starts, you can navigate to [localhost:3300](http://localhost:3300) and test every endpoint in the API. Every endpoint is documented automatically by [Flask-Restx](https://flask-restx.readthedocs.io/en/latest/index.html)

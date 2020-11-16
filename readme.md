## Todo app with python

Todo app is simple and handy small application written in python with help of  [Django](https://www.djangoproject.com/), 
[Django channels](https://channels.readthedocs.io/en/latest/), 
[Celery](https://docs.celeryproject.org/en/master/index.html), and 
[Postgresql](https://www.postgresql.org/).


#### Installation
Todo app requires [python](https://python.org/) v3.7+ to run.

Required python packages defined in requirements.txt file. 
Create virtual environment and install the packages with commands:
```sh
$ cd py_todo
$ python -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

#### Run the app 
To run application set database connections properly in py_todo/setting.py file.
Then migrate migrations and start the development server with commands:
```sh
$ python3 manage.py migrate
$ python3 manage.py migrate --database=comment
$ python3 manage.py runserver
```


To start celery task worker run:
```sh
$ celery -A py_todo worker -l info
```
#### Notes

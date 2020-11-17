### Todo app - The task sharing application with python

Todo app is a simple task sharing application written in python with the help of [Django](https://www.djangoproject.com/), [Django channels](https://channels.readthedocs.io/en/latest/), [Celery](https://docs.celeryproject.org/en/master/index.html), and [PostgreSQL](https://www.postgresql.org/).

Users can add, edit, delete, and read tasks, assign them to other users using email or username. Every task has a title, deadline, and description. Assigned users automatically informed by mail about the deadline before 10 minutes from the deadline. Authors and assigned users are able to add, edit, and delete comments to the task with the help of live updates without refreshing the page. The author can disable adding a comment to the task for a specific user when assigning it, also delete all posted task comments.

#### Installation
Todo app requires [python](https://python.org/) v3.7+ to run. Required python packages defined in requirements.txt file, create virtual environment and install the packages.

```sh
$ cd py_todo
$ python -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

#### Run the app 
To run the application set database connections in the py_todo/setting.py file, then migrate databases and start the development server.

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
I have created the same application using Laravel and MySQL, check it out from [here](https://github.com/thesafaraliyev/tasksparrow)

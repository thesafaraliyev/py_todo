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

>Todo app yazmaq lazımdır. Hər taskın adı, açıqlaması, və bitmə tarixi var. Bitmə tarixindən 10 dəq öncə xatırlatma email-i göndərmək lazımdır istifadəçiyə. Emailləri asinxron göndərmək üçün celery task istifadə etməyiniz məsləhətdir. celery broker olaraq rabbitmq ya redis-i istifadə etməkdə sərbəstsiniz

>By default olaraq tasklar ancaq onu yaradan istifadəçiyə görünür, digər istifadəçilər tərəfindən görünmür. Lakin istifadəçi digər istifadəçi ilə taskı, onun username və ya email ünvanını yazaraq paylaşa bilir. Bu zaman 2 formatda paylaşma mümkündür yalnız taskı görmək, və ya həm görmək həm də şərh yazmaq imkanı. Taskın details səhifəsində şərhlər realtime olaraq socket ilə yazılır, yəni yazılan şərhlər anlıq olaraq qarşı tərəfdə görünməlidir (django channels istifadə etməyi məsləhət görərdim).

>Database olaraq postgresql seçin. Application-u docker (docker-compose) ilə serve edin.

>1) Əgər mümkün olsa şərhləri əsas DB-də yox ayrıca bir DB-də store etməyə çalışın. (django multi-database feature)
>2) Mümkün olsa taskın müəllifi fayla yazılan şərhləri silə bilməlidir.
>3) Mümkün olsa şərhin müəllifi öz şərhini həm silə bilməli, həm də edit edə bilməlidir.

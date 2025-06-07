# Django Postgres Lock

A [Django](https://www.djangoproject.com/) management command which will run a command inside a
Postgres lock, ensuring that only a single instance of the inner command will run.

## Installation

Using [pip](https://pip.pypa.io/):

```console
$ pip install django-postgres-lock
```

Edit your Django project's settings module, and add the application to ``INSTALLED_APPS``:

```python
INSTALLED_APPS = [
    # ...
    "postgres_lock",
    # ...
]
```

## Usage

To run clearsessions with the default lock:

```console
$ ./manage.py command_lock -- ./manage.py clearsessions
```

To use a unique lock for this task:

```console
$ ./manage.py command_lock --name clearsessions -- ./manage.py clearsessions
```

To exit immediately if a lock can't be acquired:

```console
$ ./manage.py command_lock --try --name clearsessions -- ./manage.py clearsessions
```

To ignore a lock failure and return a successful exit code:

```console
$ ./manage.py command_lock --try --ignore-fail --name clearsessions -- ./manage.py clearsessions
```

Django Postgres Lock
====================

A Django_ management command which will run a command inside a Postgres lock, ensuring that only a
single instance of the inner command will run.

.. _Django: https://www.djangoproject.com/

Installation
------------

Using pip_:

.. _pip: https://pip.pypa.io/

.. code-block:: console

    $ pip install django-postgres-lock

Edit your Django project's settings module, and add the application to ``INSTALLED_APPS``:

.. code-block:: python

    INSTALLED_APPS = [
        # ...
        "postgres_lock",
        # ...
    ]

Usage
-----

To run clearsessions with the default lock:

.. code-block:: console

    $ ./manage.py command_lock -- ./manage.py clearsessions

To use a unique lock for this task:

.. code-block:: console

    $ ./manage.py command_lock --name clearsessions -- ./manage.py clearsessions

To exit immediately if a lock can't be acquired:

.. code-block:: console

    $ ./manage.py command_lock --try --name clearsessions -- ./manage.py clearsessions

To ignore a lock failure and return a successful exit code:

.. code-block:: console

    $ ./manage.py command_lock --try --ignore-fail --name clearsessions -- ./manage.py clearsessions

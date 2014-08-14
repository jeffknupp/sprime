sandman
=======

sandman is a RESTful API service provider for legacy (existing)
databases. Why is that useful? Imagine you're working for AnonymousCorp
and need to access Group Y's data, which is presented to you through
some horrible API or GUI. Wouldn't it be nice if you could just interact
with that database through a REST API?

More than that, imagine if you could interact with the database through
a REST API **and no one had to write any code**. No boilerplate ORM
code, no database connection logic. Nothing. Sandman can be run as a
command-line tool (``sandmanctl``) that just takes your database
information as parameters, then auto-magically connects to your it,
introspects the schema, generates a REST API, and starts the server.

Quickstart
----------

Install sandman using ``pip``: ``$ pip install sandman``. This provides
the script ``sandmanctl``, which just takes the database URI string,
described
`here <http://docs.sqlalchemy.org/en/rel_0_9/core/engines.html>`__. For
example, to connect to a SQLite database in the same directory you're
running the script, you would run:

.. code:: bash

    $ sandmanctl sqlite+pysqlite:///database_file_name

To connect to a PostgreSQL database, make sure you install a driver like
``psycopg2`` using ``pip``, then use the following connection string:

.. code:: bash

    $ sandmanctl postgresql+psycopg2://scott:tiger@localhost/mydatabase

Again, see `the SQLAlchemy
documentation <http://docs.sqlalchemy.org/en/rel_0_9/core/engines.html>`__
for a more comprehensive discussion of connection strings.

Supported Databases
-------------------

sandman supports all databases that the underlying ORM, SQLAlchemy,
supports. Presently, that includes:

-  MySQL
-  PostgreSQL
-  Oracle
-  Microsoft SQL Server
-  SQLite
-  Sybase
-  Drizzle
-  Firebird

Third-party packages extend support to:

-  IBM DB2
-  Amazon Redshift
-  SQL Anywhere
-  MonetDB

REST API Features
-----------------

The RESTful API service comes with the following features:

-  Proper support for all HTTP methods
-  


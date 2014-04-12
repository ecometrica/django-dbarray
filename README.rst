===============
Django dbarray
===============

Django model fields that store lists of values, implemented using the PostgreSQL ``ARRAY`` type.

Requirements
============

* PostgreSQL
* psycopg2
* Django >= 1.2

The ARRAY db type is PostgreSQL specific, so these model fields currently
work only on PostgreSQL with psycopg2.  A ``FieldError`` will be raised if the
field is used with another database.

This package has been tested with Django versions 1.2 through 1.6, inclusive.

Fields
================

The field types defined in the ``dbarray`` module are listed in the table below,
along with each field's parent class (from ``django.db.models``), and the data
type of the postgresql column it will create.

Each field takes the same arguments as its parent class.

=================== =================== ================
Field Type          Parent Class        Postgresql Type
------------------- ------------------- ----------------
IntegerArrayField   IntegerField        integer[]
FloatArrayField     FloatField          double precision[]
TextArrayField      TextField           text[]
CharArrayField      CharField           character varying[]
DateArrayField      DateField           date[]
=================== =================== ================

Custom Fields
==============

To define a new array field for a base field type ``FooField``::

    import dbarray

    class FooArrayField(dbarray.ArrayFieldBase, FooField):
        __metaclass__ = dbarray.ArrayFieldMetaclass

This may or may not work depending on a few factors.  You might, for example, need
to override the db_type method to make it put the ``[]`` in the right spot in the column
type used in generated SQL.

Another issue that may arise when performing lookups with array fields
is that PostgreSQL may get the query parameter as a data type
that isn't compatible with the type of the db column (for example text[]
instead of varchar[]).  Then you will get an error like the following::

    DatabaseError: operator does not exist: character varying[] = text[]
    LINE 1: ... FROM "dbarray_chars" WHERE "dbarray_chars"."arr" = ARRAY['A...
                                                                 ^
    HINT:  No operator matches the given name and argument type(s). You might need to add explicit type casts.

You can rectify this by setting ``cast_lookups = True`` on your
``ArrayFieldBase`` subclass, which instructs it to add an explicit type cast
to the SQL query.

Look in the source code for more examples of how to handle issues with new
ArrayField types.

Running the tests
=================

Versions of Django prior to 1.6 require
`django-discover-runner <https://pypi.python.org/pypi/django-discover-runner>`_.
Install it with::

    pip install -U django-discover-runner

The default tests also require a Postgres database named ``dbarray`` running on
localhost. See the test configuration in dbarray/tests/run.py.

You can run the test suite with::

    python dbarray/tests/run.py


Version History
===============

Version 0.2
--------------------------------
:Released: October 17, 2013

The fields raise a FieldError exception if used on a database other than
PostgreSQL.  (This was the original behavior)

Version 0.1
--------------------------------
:Released: October 16, 2013

Added tests and fixes for lookups and DateArrayField.

Version 0.0.1
--------------------------------
:Released: January 10, 2011

Initial release

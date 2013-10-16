A Django model field that stores lists of values. Implemented using the PostgreSQL array type.

============
Requirements
============

* Postgresql
* psycopg2
* Django >= 1.2
 
The ARRAY db type is PostgreSQL specific, so these model fields currently
work only on PostgreSQL/psycopg2.  It has been tested on all major versions
of Django (currently 1.2 through 1.6 inclusive).

==========
Usage
==========

Four field types are defined in the ``dbarray`` module::

    from django.db import models
    
    import dbarray

    class Foo(models.Model):
        
        numlist = dbarray.IntegerArrayField()
        floatlist = dbarray.FloatArrayField(null=True)
        textlist = dbarray.TextArrayField(
            help_text="Fields take the same arguments as their corresponding Django fields.")
        charlist = dbarray.CharArrayField(max_length=5)

==============
Custom fields
==============

To define an array type based on a field other than Integer, Float, Text, or Char::

    import dbarray
    
    class FooArrayField(dbarray.ArrayFieldBase, FooField):
        __metaclass__ = dbarray.ArrayFieldMetaclass
        
This may or may not work depending on a few factors.  You might, for example, need
to override the db_type method to make it put the ``[]`` in the right spot in the column
type used in generated SQL.

Another issue that may arise when performing lookups with array fields 
is that PostgreSQL may get the query parameter with a different data type
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


===============
Version History
===============

Version 0.1 - October 16, 2013

Added tests and fixes for lookups and DateArrayField.

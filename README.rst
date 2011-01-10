A Django model field that stores lists of values. Implemented using the PostgreSQL array type.

==========
Usage
==========

Note that this field currently works only on Postgres/psycopg2. Requires Django >= 1.2.

Four field types are defined in the ``dbarray`` module::

    from django.db import models
    
    import dbarray

    class Foo(models.Model):
        
        numlist = dbarray.IntegerArrayField()
        floatlist = dbarray.FloatArrayField(null=True)
        textlist = dbarray.TextArrayField(
            help_text="Fields take the same arguments as their corresponding Django fields.")
        charlist = dbarray.CharArrayField(max_length=5)

==========
Custom fields
==========

To define an array type based on a field other than Integer, Float, Text, or Char::

    import dbarray
    
    class FooArrayField(dbarray.ArrayFieldBase, FooField):
        __metaclass__ = dbarray.ArrayFieldMetaclass
        
This may or may not work depending on a few factors; you might, for example, need
to override the db_type method to make it add ``[]`` to right spot in the column
type used in generated SQL.
import sys

from django.core.exceptions import FieldError, ValidationError
from django.db import models
from django.utils.encoding import smart_text
from collections import deque

PY2 = sys.version_info[0] == 2
if not PY2:
    string_types = (str,)
else:
    string_types = basestring

def add_metaclass(metaclass):
    """Class decorator for creating a class with a metaclass.

    from https://github.com/kelp404/six/blob/1.4.1/six.py
    """
    def wrapper(cls):
        orig_vars = cls.__dict__.copy()
        orig_vars.pop('__dict__', None)
        orig_vars.pop('__weakref__', None)
        for slots_var in orig_vars.get('__slots__', ()):
            orig_vars.pop(slots_var)
        return metaclass(cls.__name__, cls.__bases__, orig_vars)
    return wrapper

__all__ = (
        'ArrayFieldBase',
        'ArrayFieldMetaclass',
        'IntegerArrayField',
        'FloatArrayField',
        'TextArrayField',
        'CharArrayField',
        'DateArrayField',
    )

def require_postgres(connection):
    engine = connection.settings_dict['ENGINE']
    if 'psycopg2' not in engine and 'postgis' not in engine:
        raise FieldError("Array fields are currently implemented only for PostgreSQL/psycopg2")

class Cast(object):
    """
    A utility class which allows us to slip type-casts into the SQL query
    """
    def __init__(self, value, get_db_type):
        self.value = value
        self.get_db_type = get_db_type

    def as_sql(self, qn, connection):
        db_type = self.get_db_type(connection=connection)
        cast = '%%s::%s' % db_type
        return cast, [self.value] 

class ArrayFieldBase(object):
    """Django field type for an array of values. Supported only on PostgreSQL.
    
    This class is not meant to be instantiated directly; instead, field classes
    should inherit from this class and from an appropriate Django model class.
    """
    
    _south_introspects = True
    cast_lookups = False
    
    def db_type(self, connection):
        require_postgres(connection)
        return super(ArrayFieldBase, self).db_type(connection=connection) + '[]'
        
    def to_python(self, value):
        # psycopg2 already supports array types, so we don't actually need to serialize
        # or deserialize
        if value is None:
            return None
        if not isinstance(value, (list, tuple, set, deque,)):
            try:
                iter(value)
            except TypeError:
                raise ValidationError("An ArrayField value must be None or an iterable.")
        s = super(ArrayFieldBase, self)
        return [s.to_python(x) for x in value]
            
    def get_prep_value(self, value):
        if value is None:
            return None
        s = super(ArrayFieldBase, self)
        return [s.get_prep_value(v) for v in value]
        
    def get_db_prep_lookup(self, lookup_type, value, connection, prepared=False):
        if not prepared:
            value = self.get_prep_lookup(lookup_type, value)
        if not self.cast_lookups:
            return [value]
        return Cast(value, self.db_type)

    def run_validators(self, value):
        if value is None:
            super(ArrayFieldBase, self).run_validators(value)
        else:
            for v in value:
                super(ArrayFieldBase, self).run_validators(v)
                
class ArrayFieldMetaclass(models.SubfieldBase):
    pass

def array_field_factory(name, fieldtype, module=ArrayFieldBase.__module__):
    return ArrayFieldMetaclass(name, (ArrayFieldBase, fieldtype),
        {'__module__': module,
        'description': "An array, where each element is of the same type "\
        "as %s." % fieldtype.__name__})
        
# If you want to make an array version of a field not covered below, this is
# the easiest way:
#
# On python 2:
#
# class FooArrayField(dbarray.ArrayFieldBase, FooField):
#     __metaclass__ = dbarray.ArrayFieldMetaclass
#
# On python 3:
#
# class FooArrayField(dbarray.ArrayFieldBase, FooField, metaclass=dbarray.ArrayFieldMetaclass):
#     pass
#
# On both (with six):
#
# @six.add_metaclass(dbarray.ArrayFieldMetaclass)
# class FooArrayField(dbarray.ArrayFieldBase, FooField):
#     pass

IntegerArrayField = array_field_factory('IntegerArrayField', models.IntegerField)
TextArrayField = array_field_factory('TextArrayField', models.TextField)


@add_metaclass(ArrayFieldMetaclass)
class FloatArrayField(ArrayFieldBase, models.FloatField):
    cast_lookups = True


@add_metaclass(ArrayFieldMetaclass)
class CharArrayField(ArrayFieldBase, models.CharField):
    cast_lookups = True
    def get_prep_value(self, value):
        if isinstance(value, string_types):
            return [value]
        if value is None:
            return None
        if not isinstance(value, (list, tuple, set, deque,)):
            raise ValidationError("An ArrayField value must be None or an iterable.")
        return list(map(smart_text, value))


class DateField(models.DateField):
    def get_prep_value(self, value):
        # make sure the right to_python() gets called here
        return super(DateField, self).to_python(value)


@add_metaclass(ArrayFieldMetaclass)
class DateArrayField(ArrayFieldBase, DateField):
    def get_db_prep_value(self, value, connection, prepared=False):
        # Casts dates into the format expected by the backend
        # Don't use connection.ops.value_to_db_date, it won't work
        if not prepared:
            value = self.get_prep_value(value)
        return value

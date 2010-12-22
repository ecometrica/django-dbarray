from django.core.exceptions import FieldError, ValidationError
from django.db import models
from django.utils.importlib import import_module

class ArrayField(models.Field):
    """Django field type for an array of values.
    
    Values can be of any standard database type. Supported only on PostgreSQL."""
    
    __metaclass__ = models.SubfieldBase
    
    description = "An array of values (of any single database type)"
    
    def __init__(self, *args, **kwargs):
        """Takes one required keyword argument, fieldtype, which is the class of the 
        field type we want an array of.
        
        All other arguments will be passed to the field type.
        
        e.g. ArrayField(fieldtype=models.CharField, max_length=20)
        
        """
        
        self.fieldclass = kwargs.pop('fieldtype', None)
        super(ArrayField, self).__init__()
        
        # For the fieldtype argument, as well as a class object,
        # we accept a string of full class path.
        # e.g. "django.db.models.field.IntegerField"
        # This is in order to play nicely with South
        if isinstance(self.fieldclass, basestring):
            components = self.fieldclass.split('.')
            classname = components.pop()
            module = import_module('.'.join(components))
            self.fieldclass = getattr(module, classname)
            
        if not isinstance(self.fieldclass, type) \
          and issubclass(self.fieldclass, models.Field):
            raise FieldError("ArrayField must be given Field instance as a "
                "keyword argument called fieldtype")
                
        self.fieldtype = self.fieldclass(*args, **kwargs)
        self.validators = self.fieldtype.validators
        self.default = kwargs.pop('default', None)
    
    def db_type(self, connection):
        if 'post' not in connection.settings_dict['ENGINE']:
            raise FieldError("ArrayField is currently implemented only for PostgreSQL")
        return self.fieldtype.db_type(connection=connection) + '[]'
        
    def to_python(self, value):
        # psycopg2 already supports array types, so we don't actually need to serialize
        # or deserialize
        if not isinstance(value, (list, tuple)):
            raise ValidationError("This value must be an array.")
        return [self.fieldtype.to_python(x) for x in value]
        
    def get_db_prep_value(self, value, connection, prepared=False):
        if 'post' not in connection.settings_dict['ENGINE']:
            raise FieldError("ArrayField is currently implemented only for PostgreSQL")
        return [self.fieldtype.get_db_prep_value(value=v, connection=connection, prepared=prepared)
            for v in value]
            
    def get_prep_value(self, value):
        return [self.fieldtype.get_prep_value(v) for v in value]
        
    def pre_save(self, model_instance, add):
        return self.fieldtype.pre_save(model_instance, add)
        
    def get_prep_lookup(self, lookup_type, value):
        return self.fieldtype.get_prep_lookup(lookup_type, value)
        
    def get_db_prep_lookup(self, lookup_type, value, connection, prepared=False):
        return self.fieldtype.get_db_prep_lookup(lookup_type, value, connection, prepared)
                
    def south_field_triple(self):
        "Returns a suitable description of this field for South."
        from south.modelsinspector import introspector
        parent_field_class = self.fieldclass.__module__ + "." + self.fieldclass.__name__
        our_field_class = self.__class__.__module__ + "." + self.__class__.__name__
        args, kwargs = introspector(self.fieldtype)
        kwargs['fieldtype'] = repr(parent_field_class)
        return (our_field_class, args, kwargs)
        
    def run_validators(self, value):
        for v in value:
            super(ArrayField, self).run_validators(v)
        
    
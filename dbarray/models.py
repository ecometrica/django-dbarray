from django.db import models

from .fields import *

class Integers(models.Model):
    arr = IntegerArrayField(null=True)

class Floats(models.Model):
    arr = FloatArrayField(null=True)

class Chars(models.Model):
    arr = CharArrayField(max_length=10, null=True)

class Texts(models.Model):
    arr = TextArrayField(null=True)

class Dates(models.Model):
    arr = DateArrayField(null=True)

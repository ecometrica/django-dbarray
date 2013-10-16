from datetime import date

from django import test
from django.core.exceptions import ValidationError

from .models import *

class ArrayTestMixin(object):
    def test_create_get(self):
        o = self.model.objects.create(arr=self.arr)
        o = self.model.objects.get(id=o.id)
        self.assertEqual(o.arr, self.arr)

    def test_create_lookup(self):
        a = self.model.objects.create(arr=self.arr)
        b = self.model.objects.get(arr=self.arr)
        self.assertEqual(a.id, b.id)

    def test_create_save_get(self):
        a = self.model.objects.create(arr=self.arr)
        newarr = self.arr[:len(self.arr)/2]
        a.arr = newarr
        a.save()
        b = self.model.objects.get(id=a.id)
        self.assertEqual(a.arr, b.arr)

    def test_create_update_get(self):
        o = self.model.objects.create(arr=self.arr)
        newarr = self.arr[-1::-1]
        self.model.objects.filter(id=o.id).update(arr=newarr)
        o = self.model.objects.get(id=o.id)
        self.assertEqual(o.arr, newarr)

    def test_create_lookup_update_get(self):
        o = self.model.objects.create(arr=self.arr)
        qset = self.model.objects.filter(arr=self.arr)
        newarr = self.arr[:len(self.arr)/2]
        qset.update(arr=newarr)
        o = self.model.objects.get(id=o.id)
        self.assertEqual(o.arr, newarr)

    def test_null(self):
        o = self.model.objects.create()
        o = self.model.objects.get(id=o.id)
        self.assertEqual(o.arr, None)

        c = self.model.objects.filter(arr__isnull=True).count()
        self.assertEqual(c, 1)

    def test_noniterable(self):
        val = self.arr
        while True:
            try:
                val = val[0]
            except TypeError:
                break
        method = self.model.objects.create
        self.assertRaises(ValidationError, method, arr=val)

class IntegerArrayTestCase(ArrayTestMixin, test.TestCase):
    arr = [1,4,2,7]
    model = Integers

class FloatArrayTestCase(ArrayTestMixin, test.TestCase):
    arr = [3.5, 6.0, 8.25, 9.875]
    model = Floats

class CharArrayTestCase(ArrayTestMixin, test.TestCase):
    arr = ['Adrian', 'Jacob', 'Simon', 'Wilson', 'Malcolm']
    model = Chars
    test_noniterable = None

class TextArrayTestCase(CharArrayTestCase):
    model = Texts

class DateArrayTestCase(ArrayTestMixin, test.TestCase):
    arr = [date(1910, 1, 23),
            date(1953, 5, 16),
            date(2005, 7, 12),
            date(2010, 12, 22)]
    model = Dates

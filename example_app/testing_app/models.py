from django.db import models
from dirtyfields import DirtyFieldsMixin

class TestModel(DirtyFieldsMixin, models.Model):
    """A simple test model to test dirty fields mixin with"""
    boolean = models.BooleanField(default=True)
    characters = models.CharField(blank=True, max_length=80)

class TestRelModel(DirtyFieldsMixin, models.Model):
    test_model = models.ForeignKey(TestModel)
    characters = models.CharField(blank=True, max_length=80)

from django.core.management.color import no_style
from django.db import models
from django.test import TestCase
from django.conf import settings
from django.core.management import call_command
from django.db.models.loading import load_app
from django.db import connection, transaction

from testing_app.models import TestModel

class DirtyFieldsMixinTestCase(TestCase):

    def test_dirty_fields(self):
        tm = TestModel()
        # initial state shouldn't be dirty
        self.assertEqual(tm.get_dirty_fields(), {})

        # changing values should flag them as dirty
        tm.boolean = False
        tm.characters = 'testing'
        self.assertEqual(tm.get_dirty_fields(), {
            'boolean': True,
            'characters': ''
        })

        # resetting them to original values should unflag
        tm.boolean = True
        self.assertEqual(tm.get_dirty_fields(), {
            'characters': ''
        })

    def test_sweeping(self):
        tm = TestModel()
        tm.boolean = False
        tm.characters = 'testing'
        self.assertEqual(tm.get_dirty_fields(), {
            'boolean': True,
            'characters': ''
        })
        tm.save()
        self.assertEqual(tm.get_dirty_fields(), {})

    def test_revert(self):
        tm = TestModel()
        tm.boolean = False
        tm.characters = 'testing'
        self.assertEqual(tm.get_dirty_fields(), {
            'boolean': True,
            'characters': ''
        })
        tm.revert()
        self.assertEqual(tm.get_dirty_fields(), {})

    def test_revert_with_fields(self):
        tm = TestModel()
        tm.boolean = False
        tm.characters = 'testing'
        self.assertEqual(tm.get_dirty_fields(), {
            'boolean': True,
            'characters': ''
        })
        tm.revert(field_names=['boolean'])
        self.assertEqual(tm.get_dirty_fields(), {
            'characters': ''
        })

    def test_model_init_kwargs(self):
        tm = TestModel(boolean=False, characters='testing')
        self.assertEqual(tm.get_dirty_fields(), {
            'boolean': True,
            'characters': ''
        })

    def test_manager_returns_clean_model(self):
        tm = TestModel.objects.create(boolean=True, characters='testing')
        tm = TestModel.objects.get(pk=tm.pk)
        self.assertEqual(tm.get_dirty_fields(), {})

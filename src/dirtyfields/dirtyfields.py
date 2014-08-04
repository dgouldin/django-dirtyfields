# Adapted from http://stackoverflow.com/questions/110803/dirty-fields-in-django

from django.db.models.signals import post_save
import copy


class DirtyFieldsMixin(object):
    def __init__(self, *args, **kwargs):
        super(DirtyFieldsMixin, self).__init__(*args, **kwargs)
        post_save.connect(reset_state,
                          sender=self.__class__,
                          dispatch_uid='{}-DirtyFieldsMixin-sweeper'.format(
                              self.__class__.__name__))
        reset_state(sender=self.__class__, instance=self)

    def _as_dict(self, do_copy=False):
        if do_copy:
            getter = lambda value: copy.copy(value)
        else:
            getter = lambda value: value

        return dict([(f.name, getter(getattr(self, f.name)))
                     for f in self._meta.local_fields
                     if not f.rel])

    def get_dirty_fields(self):
        new_state = self._as_dict()

        return dict([(key, value)
                     for key, value in self._original_state.items()
                     if value != new_state[key]])

    def is_dirty(self):
        # in order to be dirty we need to have been saved at least once, so we
        # check for a primary key and we need our dirty fields to not be empty
        if not self.pk:
            return True
        return {} != self.get_dirty_fields()

    def revert(self, field_names=None):
        """
        Revert given fields back to their original state. If field_names is
        None, revert all fields.
        """
        field_names = field_names or self._original_state.keys()
        for field_name in field_names:
            setattr(self, field_name,
                    copy.copy(self._original_state[field_name]))


def reset_state(sender, instance, **kwargs):
    instance._original_state = instance._as_dict(True)

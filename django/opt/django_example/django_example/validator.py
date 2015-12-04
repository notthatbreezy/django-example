from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _


class CannotStartWithA(object):

    def validate(self, password, user=None):
        if password.startswith('a'):
            raise ValidationError(
                _('Passwords cannot start with the letter "a"!'),
                code='wrong_letter'
            )

    def get_help_text(self):
        return _('Your password started with the letter "a"! That is a huge security risk!')

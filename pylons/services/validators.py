import re
from marshmallow.validate import Validator
from marshmallow.exceptions import ValidationError



class PartyName(Validator):
    """Validates a party name. A party can be a person or an organization.
    """
    # messages
    message_min = 'Must be at least {min} characters long.'
    message_bad_chars = 'Must not contain digits or symbols.'
    message_all_vowels = 'Must not be all vowels.'

    # re
    INVALID_CHARS = re.compile('[0-9$-/:-?{-~!"^_`\[\]]+')
    ALL_VOWELS = re.compile('^[aeiou]+$', re.IGNORECASE)


    def __init__(self, min=3, for_person=True, error=None):
        self.min = min
        self.error = error
        self.for_person = for_person

    def _repr_args(self):
        return 'min={0!r}, for_person={1!r}'.format(self.min, self.for_person)

    def _format_error(self, value, message):
        return (self.error or message).format(
            min=self.min, for_person=self.for_person
        )

    def __call__(self, value):
        """Validates a name assumed to be that of a person against some simple
        checks such as:
            - not containing any digits
            - shouldn't be all vowels or consonants

        :param return_on_error: Indicates whether to return on the first error
            i.e. first failed validation encountered or to proceed and discover
            more error i.e. failing validations if there are more.
        """
        if self.min is not None and len(value) < self.min:
            message = self.message_min
            raise ValidationError(self._format_error(value, message))

        if self.for_person:
            if self.INVALID_CHARS.search(value):
                message = self.message_bad_chars
                raise ValidationError(self._format_error(value, message))
            elif self.ALL_VOWELS.match(value):
                message = self.message_all_vowels
                raise ValidationError(self._format_error(value, message))
        return value

"""Defines schemas used to defined expected fields and perform data validation.
"""
import re
from marshmallow import (
    Schema, fields, post_load,
    ValidationError, validate as val
    )
from zope.interface import implementer
from elixr2.auth.schemas import DefaultRegistrationSchema, DefaultAuthSchemas
from .validators import PartyName



class RegistrationSchema(DefaultRegistrationSchema):
    """Schema to specify and validate the fields required to perform a user
    registration.

    :field first_name: user first name
    :field last_name: user last name
    :field email: user email
    :field password: user password
    :field password2: used to confirm user password
    """
    first_name = fields.String(required=True, validate=PartyName())
    last_name = fields.String(required=True, validate=PartyName())


class AuthSchemas(DefaultAuthSchemas):

    def registration_schema(self, ctx):
        """Defines the fields and validation rules for the user registration UI.
        """
        schema = RegistrationSchema()
        schema.context['ctx'] = ctx
        return schema

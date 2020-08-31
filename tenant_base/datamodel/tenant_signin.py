#  Copyright (c) Akretion 2020
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo.addons.datamodel import fields
from odoo.addons.datamodel.core import Datamodel
from marshmallow_objects import validates_schema
from marshmallow.exceptions import ValidationError


class TenantSigninInput(Datamodel):
    _name = "tenant.signin.input"

    # @validates_schema  TODO reactivate
    # def validate_signin(self, data):
    #     backend = data.backend.split(",")
    #     correct = (
    #         len(backend) == 2
    #         and isinstance(backend[0], str)
    #         and isinstance(backend[1], int)
    #     )
    #     if not correct:
    #         raise ValidationError()

    login = fields.Str(required=True)
    password = fields.Str(required=True)
    backend = fields.NestedModel("tenant.backend", required=True)


class TenantSigninOutput(Datamodel):
    _name = "tenant.signin.output"

    token = fields.Str(required=True)

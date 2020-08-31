#  Copyright (c) Akretion 2020
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo.addons.datamodel import fields
from odoo.addons.datamodel.core import Datamodel


class TenantSignupInput(Datamodel):
    _name = "tenant.signup.input"

    login = fields.Str(required=True)
    password = fields.Str(required=True)
    backend = fields.NestedModel("tenant.backend", required=True)


class TenantSignupOutput(Datamodel):
    _name = "tenant.signup.output"

    result = fields.Boolean(required=True)

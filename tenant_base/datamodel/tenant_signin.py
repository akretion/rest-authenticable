#  Copyright (c) Akretion 2020
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo.addons.datamodel import fields
from odoo.addons.datamodel.core import Datamodel


class TenantSigninInput(Datamodel):
    _name = "tenant.signin.input"

    login = fields.Str(required=True)
    password = fields.Str(required=True)
    backend = fields.NestedModel("tenant.backend", required=True)


class TenantSigninOutput(Datamodel):
    _name = "tenant.signin.output"

    token = fields.Str(required=True)

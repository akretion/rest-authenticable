#  Copyright (c) Akretion 2020
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo.addons.datamodel import fields
from odoo.addons.datamodel.core import Datamodel


class TenantResetPwdInput(Datamodel):
    _name = "tenant.reset.pwd.input"

    tenant_identifier = fields.Str(required=True)


class TenantSigninOutput(Datamodel):
    _name = "tenant.reset.pwd.output"

    result = fields.Boolean(required=True)

#  Copyright (c) Akretion 2020
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo.addons.datamodel import fields
from odoo.addons.datamodel.core import Datamodel


class TenantSignoutInput(Datamodel):
    _name = "tenant.signout.input"

    tenant_identifier = fields.Str(required=True)


class TenantSignoutOutput(Datamodel):
    _name = "tenant.signout.output"

    result = fields.Boolean(required=True)

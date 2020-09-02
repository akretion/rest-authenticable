#  Copyright (c) Akretion 2020
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo.addons.datamodel import fields
from odoo.addons.datamodel.core import Datamodel


class TenantChangePwdInput(Datamodel):
    _name = "tenant.change.pwd.input"

    tenant_identifier = fields.Str(
        required=True
    )  # TODO jarter tous les tenant_identifier
    password = fields.Str(required=True)


class TenantChangePwdOutput(Datamodel):
    _name = "tenant.change.pwd.output"

    result = fields.Boolean(required=True)

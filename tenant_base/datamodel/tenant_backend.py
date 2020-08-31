#  Copyright (c) Akretion 2020
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo.addons.datamodel import fields
from odoo.addons.datamodel.core import Datamodel


class TenantBackend(Datamodel):
    _name = "tenant.backend"

    backend_name = fields.Str(required=True)
    backend_id = fields.Int(required=True)

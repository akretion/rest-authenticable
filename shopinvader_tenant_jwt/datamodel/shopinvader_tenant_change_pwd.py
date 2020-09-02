#  Copyright (c) Akretion 2020
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo.addons.datamodel.core import Datamodel


class ShopinvaderTenantChangePwdInput(Datamodel):
    _name = "shopinvader.tenant.change.pwd.input"
    _inherit = "tenant.change.pwd.input"


class ShopinvaderTenantChangePwdOutput(Datamodel):
    _name = "shopinvader.tenant.change.pwd.output"
    _inherit = "tenant.change.pwd.output"

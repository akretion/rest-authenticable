#  Copyright (c) Akretion 2020
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo.addons.datamodel.core import Datamodel


class ShopinvaderTenantSigninInput(Datamodel):
    _inherit = "tenant.signin.input"
    _name = "shopinvader.tenant.signin.input"


class ShopinvaderTenantSigninOutput(Datamodel):
    _inherit = "tenant.signin.output"
    _name = "shopinvader.tenant.signin.output"

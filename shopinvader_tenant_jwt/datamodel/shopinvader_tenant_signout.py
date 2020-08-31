#  Copyright (c) Akretion 2020
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo.addons.datamodel import fields
from odoo.addons.datamodel.core import Datamodel


class ShopinvaderTenantSignoutInput(Datamodel):
    _inherit = "tenant.signout.input"
    _name = "shopinvader.tenant.signout.input"


class ShopinvaderTenantSignoutOutput(Datamodel):
    _inherit = "tenant.signout.output"
    _name = "shopinvader.tenant.signout.output"

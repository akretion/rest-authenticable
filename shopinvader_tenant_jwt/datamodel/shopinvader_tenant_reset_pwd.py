#  Copyright (c) Akretion 2020
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo.addons.datamodel import fields
from odoo.addons.datamodel.core import Datamodel


class ShopinvaderTenantResetPwdInput(Datamodel):
    _inherit = "tenant.reset.pwd.input"
    _name = "shopinvader.tenant.reset.pwd.input"


class ShopinvaderTenantResetPwdOutput(Datamodel):
    _inherit = "tenant.reset.pwd.output"
    _name = "shopinvader.tenant.reset.pwd.output"


class ShopinvaderTenantResetPwdLandingOutput(Datamodel):
    _name = "shopinvader.tenant.reset.pwd.landing.output"

    token = fields.Str(required=True)

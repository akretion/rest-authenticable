# Copyright 2020 Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.tenant_base.models.tenant_base import TenantBase
from odoo import models


class TenantJwt(models.AbstractModel):
    _inherit = "tenant.base"
    _name = "tenant.jwt"

    def t_sign_out(self):
        return (
            True  # this must be handled client-side, browser destroys the token cookie
        )

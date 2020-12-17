# Copyright 2020 Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models
from ..common import check_password_strength


class TenantBase(models.AbstractModel):
    _inherit = "tenant.base"

    def t_change_password(self, password):
        result = super().t_change_password(password)
        check_password_strength(password)
        return result

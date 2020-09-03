# Copyright 2020 Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models
from ..common import check_password_strength


class TenantBackendBase(models.AbstractModel):
    _inherit = "tenant.backend.base"

    def tb_sign_up(self, payload):
        result = super().tb_sign_up(payload)
        check_password_strength(payload.password)
        return result

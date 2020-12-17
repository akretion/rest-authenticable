# Copyright 2020 Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import hashlib
from odoo import models, fields, _
from odoo.exceptions import ValidationError


class TenantBase(models.AbstractModel):
    _inherit = "tenant.base"

    tenant_previous_password_hash = fields.Char()

    def _check_password_rotation(self, password):
        new_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
        if self.tenant_previous_password_hash == new_hash:
            raise ValidationError(_("Password cannot be the same as the previous one"))
        return new_hash

    def t_change_password(self, password):
        result = super().t_change_password(password)
        new_hash = self._check_password_rotation(password)
        self.tenant_previous_password_hash = new_hash
        return result

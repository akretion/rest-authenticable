# Copyright 2020 Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import hashlib
from odoo import models, _
from odoo.exceptions import ValidationError


class TenantBackendBase(models.AbstractModel):
    _name = "tenant.backend.base"
    _description = "Tenant Backend"
    _tenant_model = None

    @property
    def tenant_model(self):
        return self.env[self._tenant_model]

    def tb_sign_in(self, payload):
        self = self.sudo()
        pwd_hash = hashlib.sha256(payload.password.encode("utf-8")).hexdigest()
        tenant = self.tenant_model.search(
            [
                (self.tenant_model._tenant_login, "=", payload.login),
                (self.tenant_model._tenant_pwd_hash, "=", pwd_hash),
            ]
        )
        if tenant:
            return tenant
        else:
            raise ValidationError(_("No tenant found for these credentials"))

    def _prepare_tenant_sign_up_vals(self, payload):
        pwd_hash = hashlib.sha256(payload.password.encode("utf-8")).hexdigest()
        return {
            self.tenant_model._tenant_pwd_hash: pwd_hash,
            self.tenant_model._tenant_login: payload.login,
        }

    def tb_sign_up(self, payload):
        self = self.sudo()
        login_field = self.tenant_model._tenant_login
        already_exists = self.tenant_model.search([(login_field, "=", payload.login)])
        if already_exists:
            raise ValidationError(_("User already exists"))
        else:
            vals = self._prepare_tenant_sign_up_vals(payload)
            self.env[self._tenant_model].create(vals)
            return True

    def tb_sign_out(self, tenant):
        self = self.sudo()
        return tenant.t_sign_out()

    def tb_reset_password(self, tenant):
        self = self.sudo()
        return tenant.t_reset_password()

    def tb_change_password(self, payload, tenant):
        self = self.sudo()
        return tenant.t_change_password(payload.password)

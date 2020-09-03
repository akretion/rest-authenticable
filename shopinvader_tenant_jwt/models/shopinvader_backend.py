# Copyright 2020 Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import datetime
from odoo import models


class ShopinvaderBackend(models.Model):
    _name = "shopinvader.backend"
    _inherit = ["shopinvader.backend", "tenant.backend.jwt"]
    _tenant_model = "shopinvader.partner"

    def _find_tenant(self, tenant):
        return self.tenant_model.search(
            [(self.tenant_model._tenant_identifier, "=", tenant)]
        )

    def _get_locomotivecms_change_pwd_url(self):
        return "https://www.example.com"  # TODO

    def _jwt_send_change_pwd_email(
        self, tenant
    ):  # LocomotiveCMS URL and email should be hardcoded in template
        token = self.jwt_generate(tenant, delta=30)
        url = self._get_locomotivecms_change_pwd_url()
        return self.env.ref("shopinvader_tenant_jwt.mail_template_reset_pwd").send_mail(
            tenant.id, email_values={"url": url, "token": token}
        )

    def tb_reset_password(self, tenant):
        super().tb_reset_password(tenant)
        self = self.sudo()
        tenant = self._find_tenant(tenant)
        self._send_notification("customer_reset_password", tenant)
        self._jwt_send_change_pwd_email(tenant)
        return True

    def tb_change_password(self, payload, tenant):
        super().tb_change_password(payload, tenant)
        self = self.sudo()
        tenant = self._find_tenant(tenant)
        result = tenant.t_change_password(payload.password)
        self._send_notification("customer_change_password", tenant)
        return result

    def _prepare_tenant_external_id(self, payload):
        return payload.external_id

    def _prepare_tenant_sign_up_vals(self, payload):
        result = super()._prepare_tenant_sign_up_vals(payload)
        simple_copy = [
            "name",
            "date",
            "street",
            "street2",
            "zip",
            "city",
            "email",
        ]
        new_vals = {field: getattr(payload.address, field) for field in simple_copy}
        new_vals["backend_id"] = self.id
        new_vals["external_id"] = self._prepare_tenant_external_id(payload)
        new_vals["sync_date"] = datetime.datetime.today()
        result.update(new_vals)
        return result

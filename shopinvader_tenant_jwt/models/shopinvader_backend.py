# Copyright 2020 Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import datetime
from odoo import models


class ShopinvaderBackend(models.Model):
    _name = "shopinvader.backend"
    _inherit = ["shopinvader.backend", "tenant.backend.jwt"]
    _tenant_model = "shopinvader.partner"

    def _jwt_send_temporary_token(self, tenant):  # TODO whole workflow seems iffy
        token = self.jwt_generate(tenant, delta=30)
        url = (
            self.env["ir.config_parameter"].get_param("web.base.url")
            + "/shopinvader-partner/reset_password_landing/"
            + token.decode("utf-8")
        )
        return self.env.ref(
            "shopinvader_tenant_jwt.mail_template_temp_token"
        ).send_mail(tenant.id, email_values={"url": url})

    def tb_reset_password(self, tenant):
        self._send_notification("customer_reset_password", tenant)
        self._jwt_send_temporary_token(tenant)
        return True

    def tb_change_password(self, payload, tenant):
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

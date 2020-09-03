# Copyright 2020 Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import datetime
from odoo import models, _, fields

TIMEDELTA_DAYS = 30  # TODO put in ir.param


def check_password_is_expired(tenant, delta):
    if (
        tenant.tenant_password_last_modified + datetime.timedelta(days=delta)
        > datetime.datetime.today()
    ):
        return True


class TenantBackendBase(models.AbstractModel):
    _inherit = "tenant.backend.base"

    tenant_password_last_modified = fields.Date()

    def _prepare_tenant_sign_up_vals(self, payload):
        result = super()._prepare_tenant_sign_up_vals(payload)
        result.update({"tenant_password_last_modified": datetime.datetime.today()})
        return result

    def tb_sign_in(self, payload):
        result = super().tb_sign_in(payload)
        if check_password_is_expired(result, TIMEDELTA_DAYS):
            return self.tb_reset_password(result)
        return result

    def tb_change_password(self, payload):
        result = super().tb_change_password(payload)
        result.tenant_password_last_modified = datetime.datetime.today()

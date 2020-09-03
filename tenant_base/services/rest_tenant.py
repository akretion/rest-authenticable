# Copyright 2020 Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.addons.component.core import AbstractComponent


class RestTenantBase(AbstractComponent):
    _inherit = "base.rest.service"
    _name = "rest.tenant.base"
    _usage = "auth"

    def _find_backend_from_request(self):
        raise NotImplementedError()

    def _sign_up(self, payload):
        return (
            self.env[payload.backend.backend_name]
            .browse(payload.backend.backend_id)
            .tb_sign_up(payload)
        )

    def _sign_in(self, payload):
        return (
            self.env[payload.backend.backend_name]
            .browse(payload.backend.backend_id)
            .tb_sign_in(payload)
        )

    def _sign_out(self, backend, tenant):
        return backend.tb_sign_out(tenant)

    def _change_password(self, payload, backend, tenant):
        return backend.tb_change_password(payload, tenant)

    def _reset_password(self, payload):
        return (
            self.env[payload.backend.backend_name]
            .browse(payload.backend.backend_id)
            .tb_reset_password(payload.tenant_identifier)
        )

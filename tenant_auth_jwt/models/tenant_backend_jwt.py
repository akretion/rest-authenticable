# Copyright 2020 Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import jwt
from datetime import datetime
from odoo import fields, models, _
from odoo.exceptions import ValidationError


class TenantBackendJwt(models.AbstractModel):
    _name = "tenant.backend.jwt"
    _inherit = "tenant.backend.base"
    _description = "Tenant Backend"

    jwt_secret_key = fields.Char()

    def _jwt_get_timestamp(self, delta=10080):  # TODO + xyz
        return (
            datetime.utcnow() + datetime.datetime.timedelta(minutes=delta)
        ).timestamp()

    def jwt_verify_validity(self, token):
        if not self.jwt_secret_key:
            raise ValidationError(_("No secret key defined"))
        jwt.decode(token, verify=True, key=self.jwt_secret_key, algorithms=["HS256"])
        return True

    def jwt_generate(self, tenant, delta=10080):
        if not self.jwt_secret_key:
            raise ValidationError(_("No secret key defined"))
        payload = {
            "iss": "{},{}".format(self._name, self.id),
            "sub": "{},{}".format(tenant._name, tenant.id),
            "exp": self._jwt_get_timestamp(delta),
        }
        token = jwt.encode(payload, self.jwt_secret_key)
        return token

    def tb_sign_in(self, payload):
        return self.jwt_generate(super().tb_sign_in(payload))

    # def _find_tenant_jwt(self):
    #     tenant = request.session.httprequest.environ["JWTTOKEN"]
    #
    # def tenant_sign_out(self):
    #     self._find_tenant_jwt().sign_out()
    #
    # def tenant_reset_password(self):
    #     self._find_tenant_jwt().reset_password()
    #
    # def tenant_change_password(self):
    #     self._find_tenant_jwt().change_password(payload.password)
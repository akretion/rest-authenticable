# Copyright 2020 Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import jwt
import datetime
from odoo import fields, models, _
from odoo.exceptions import ValidationError

DEFAULT_JWT_DURATION = 10080  # 7 days in minutes


class AuthenticableBackendJwt(models.AbstractModel):
    _name = "authenticable.backend.jwt"
    _inherit = "authenticable.backend.base"
    _description = "Authenticable Backend"

    jwt_secret_key = fields.Char()

    def _jwt_get_timestamp(self, delta=DEFAULT_JWT_DURATION):
        return (
            datetime.datetime.utcnow() + datetime.timedelta(minutes=delta)
        ).timestamp()

    def jwt_verify_validity(self, token):
        if not self.jwt_secret_key:
            raise ValidationError(_("No secret key defined"))
        jwt.decode(token, verify=True, key=self.jwt_secret_key, algorithms=["HS256"])
        return True

    def jwt_generate(self, authenticable, delta=10080):
        if not self.jwt_secret_key:
            raise ValidationError(_("No secret key defined"))
        payload = {
            "iss": "{},{}".format(self._name, self.id),
            "sub": "{},{}".format(authenticable._name, authenticable.id),
            "exp": self._jwt_get_timestamp(delta),
        }
        token = jwt.encode(payload, self.jwt_secret_key)
        return token

    def sign_in(self, payload):
        return self.jwt_generate(super().sign_in(payload))

# Copyright 2020 Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import tools
from odoo.addons.component.core import AbstractComponent
from datetime import datetime, timedelta
import jwt


class BaseAuthenticableJWT(AbstractComponent):
    _inherit = "base.authenticable"
    _name = "base.authenticable.jwt"

    def _get_expire(self, directory):
        return (
            datetime.utcnow() + timedelta(minutes=directory.jwt_duration)
        ).timestamp()

    def _prepare_jwt_payload(self, partner_auth):
        return {
            "iss": partner_auth.directory_id.id,
            "sub": partner_auth.id,
            "exp": self._get_expire(partner_auth.directory_id),
        }

    def _prepare_jwt_cookie(self, partner_auth):
        directory = partner_auth.directory_id
        if not directory.jwt_secret_key:
            raise ValidationError(_("No secret key defined"))
        payload = self._prepare_jwt_payload(partner_auth)
        token = jwt.encode(payload, directory.jwt_secret_key)
        vals = {
            "value": token,
            "expires": payload["exp"],
            "httponly": True,
            "secure": True,
            "samesite": "strict",
            }
        if tools.config.get("test_enable"):
            # do not force https for test
            vals["secure"] = False
        return vals

    def _successfull_sign_in(self, partner_auth):
        response = super()._successfull_sign_in(partner_auth)
        params = self._prepare_jwt_cookie(partner_auth)
        response.set_cookie("jwt", **params)
        return response
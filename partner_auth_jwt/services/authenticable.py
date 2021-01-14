# Copyright 2020 Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from datetime import datetime, timedelta

import jwt

from odoo import _, tools
from odoo.exceptions import ValidationError

from odoo.addons.component.core import AbstractComponent


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

    def _set_jwt_cookie(self, partner_auth, response):
        params = self._prepare_jwt_cookie(partner_auth)
        response.set_cookie("jwt", **params)

    def _successfull_sign_in(self, partner_auth):
        response = super()._successfull_sign_in(partner_auth)
        self._set_jwt_cookie(partner_auth, response)
        return response

    def _sign_out(self):
        response = super()._sign_out()
        response.set_cookie("jwt", max_age=0)
        return response

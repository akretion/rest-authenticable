# Copyright 2020 Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

import jwt

from odoo import SUPERUSER_ID, _, models
from odoo.exceptions import AccessDenied, ValidationError
from odoo.http import request

_logger = logging.getLogger(__name__)


class IrHttp(models.AbstractModel):
    _inherit = "ir.http"

    @classmethod
    def _auth_method_partner_auth_jwt(cls):
        token = request.httprequest.cookies.get("jwt")
        env = request.env(user=SUPERUSER_ID)
        if not token:
            _logger.error(_("No or bad JWT, access denied"))
            raise AccessDenied()
        try:
            options = {"require": ["iss", "sub", "exp"], "verify_signature": False}
            claims = jwt.decode(token, options=options)
            directory = env["directory.auth"].browse(int(claims["iss"]))
            if not directory.jwt_secret_key:
                raise ValidationError(_("No secret key defined"))
            else:
                jwt.decode(
                    token,
                    verify=True,
                    key=directory.jwt_secret_key,
                    algorithms=["HS256"],
                )
            request.partner_auth = env["partner.auth"].browse(int(claims["sub"]))
            request.directory = directory
        except Exception as e:
            _logger.error("Problem decoding JWT, access denied")
            _logger.error("%s" % str(e))
            raise AccessDenied()
        return True

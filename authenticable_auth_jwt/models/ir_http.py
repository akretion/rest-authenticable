# Copyright 2020 Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
from odoo import models, _
from odoo.exceptions import AccessDenied
from ..common import get_jwt_token_from_header, translate_claims

_logger = logging.getLogger(__name__)


class IrHttp(models.AbstractModel):
    _inherit = "ir.http"

    @classmethod
    def _auth_method_jwt(cls):
        token = get_jwt_token_from_header()
        if not token:
            _logger.error(_("No or bad JWT, access denied"))
            raise AccessDenied()
        try:
            backend, x = translate_claims(token)
            backend.jwt_verify_validity(token)
        except Exception as e:
            _logger.error("Problem decoding JWT, access denied")
            _logger.error("%s" % str(e))
            raise AccessDenied()
        return True

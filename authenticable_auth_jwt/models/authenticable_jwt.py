# Copyright 2020 Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class AuthenticableJwt(models.AbstractModel):
    _inherit = "authenticable.base"
    _name = "authenticable.jwt"

    def sign_out(self):
        result = super().sign_out()
        return (
            True  # this must be handled client-side, browser destroys the token cookie
        )

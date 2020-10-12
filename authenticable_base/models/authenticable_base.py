# Copyright 2020 Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import hashlib
from odoo import models


class AuthenticableBase(models.AbstractModel):
    _name = "authenticable.base"
    _description = "Authenticable"

    _authenticable_login = None
    _authenticable_pwd_hash = None
    _authenticable_identifier = (
        "id"  # Note ! 1. You must ensure this is a unique constrained field
        #  2. You must ensure this is a stored, non-related field
    )

    def t_change_password(self, password):
        pwd_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
        pwd_field = self._authenticable_pwd_hash
        setattr(self, pwd_field, pwd_hash)
        return "Success"

    def t_reset_password(self):
        pass

    def t_sign_out(self):
        pass

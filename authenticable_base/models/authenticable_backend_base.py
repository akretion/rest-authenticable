# Copyright 2020 Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import hashlib
from odoo import models, _
from odoo.exceptions import ValidationError


class AuthenticableBackendBase(models.AbstractModel):
    _name = "authenticable.backend.base"
    _description = "Authenticable Backend"
    _authenticable_model = None

    @property
    def authenticable_model(self):
        return self.env[self._authenticable_model]

    def _authenticate(self, payload):
        pwd_hash = hashlib.sha256(payload.password.encode("utf-8")).hexdigest()
        authenticable = self.authenticable_model.search(
            [
                (self.authenticable_model._authenticable_login, "=", payload.login),
                (self.authenticable_model._authenticable_pwd_hash, "=", pwd_hash),
            ]
        )
        if authenticable:
            return authenticable
        else:
            raise ValidationError(_("No authenticable found for these credentials"))

    def sign_in(self, payload):
        self = self.sudo()
        return self._authenticate(payload)

    def _prepare_authenticable_sign_up_vals(self, payload):
        pwd_hash = hashlib.sha256(payload.password.encode("utf-8")).hexdigest()
        return {
            self.authenticable_model._authenticable_pwd_hash: pwd_hash,
            self.authenticable_model._authenticable_login: payload.login,
        }

    def sign_up(self, payload):
        self = self.sudo()
        login_field = self.authenticable_model._authenticable_login
        already_exists = self.authenticable_model.search([(login_field, "=", payload.login)])
        if already_exists:
            raise ValidationError(_("User already exists"))
        else:
            vals = self._prepare_authenticable_sign_up_vals(payload)
            self.env[self._authenticable_model].create(vals)
            return True

    def sign_out(self, authenticable):
        self = self.sudo()
        return authenticable.sign_out()

    def reset_password(self, authenticable):
        self = self.sudo()
        return authenticable.reset_password()

    def change_password(self, payload, authenticable):
        self = self.sudo()
        return authenticable.change_password(payload.password)

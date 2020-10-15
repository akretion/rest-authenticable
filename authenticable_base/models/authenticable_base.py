# Copyright 2020 Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import passlib
from odoo import models
from odoo.exceptions import AccessDenied

# please read passlib great documentation
# https://passlib.readthedocs.io
# https://passlib.readthedocs.io/en/stable/narr/quickstart.html#choosing-a-hash
# be carefull odoo requirements use an old version of passlib
DEFAULT_CRYPT_CONTEXT = passlib.context.CryptContext(['pbkdf2_sha512'])


class AuthenticableBase(models.AbstractModel):
    _name = "authenticable.mixin"
    _description = "Authenticable"

    _authenticable_login_field = None
    _authenticable_password_field = None

    def _crypt_context(self):
        return DEFAULT_CRYPT_CONTEXT

    def _check_no_empty(self, login, password):
        # double check by security but calling this through a service should
        # already have check this
        if not (
                isinstance(password, str) and password
                and isinstance(login, str) and login):
            _logger.warning("Invalid login/password for sign in")
            raise AccessDenied()

    def _get_hashed_password(self, login, password, backend_id):
        self.env.cr.execute(
            "SELECT id, COALESCE({}, '') FROM {} WHERE {}=%s AND backend_id=%s".format(
                self._authenticable_password_field,
                self._table,
                self._authenticable_login_field
                ),
            (login, backend_id)
        )
        hashed = self.env.cr.fetchone()
        if hashed:
            return hashed
        else:
            raise AccessDenied()

    def _set_password(self, password):
        ctx = self._crypt_context()
        self.encrypted_password = ctx.encrypt(password)

    def _sign_in(self, login, password, backend_id):
        self._check_no_empty(login, password)
        _id, hashed = self._get_hashed_password(login, password, backend_id)
        valid, replacement = self._crypt_context().verify_and_update(password, hashed)

        if replacement is not None:
            self.browse(_id).encrypted_password = replacement

        if not valid:
            raise AccessDenied()
        return self.browse(_id)

#
#    def change_password(self, password):
#        pwd_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
#        pwd_field = self._authenticable_pwd_hash
#        setattr(self, pwd_field, pwd_hash)
#        return "Success"
#
#    def reset_password(self):
#        pass
#
#    def sign_out(self):
#        pass
#
#

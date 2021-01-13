# Copyright 2020 Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models, api, registry


class TooManyLoginsExc(Exception):
    pass


class AccountBlockedExc(Exception):
    pass


class PartnerAuth(models.Model):
    _inherit = "partner.auth"

    login_attempts = fields.Integer()
    blocked_too_many_logins = fields.Boolean(
        help="Is the account blocked because of too many login attempts"
    )

    def _increment_login_attempt(self, partner):
        partner.login_attempts += 1
        self.env.cr.commit()

    def _check_too_many_login_attempts(self, directory, login):
        partner = self.env["partner.auth"].search(
            [("login", "=", login), ("directory_id", "=", directory.id)]
        )
        self._increment_login_attempt(partner)
        if partner.blocked_too_many_logins:
            raise AccountBlockedExc()
        max_login_attempts = directory.policy_login_attempts
        if max_login_attempts and partner.login_attempts > max_login_attempts:
            partner.blocked_too_many_logins = True
            raise TooManyLoginsExc()

    def _get_hashed_password(self, directory, login):
        """ _get_hashed_password implementation means
         hash exists == login exists """
        result = super()._get_hashed_password(directory, login)
        self._check_too_many_login_attempts(directory, login)
        return result

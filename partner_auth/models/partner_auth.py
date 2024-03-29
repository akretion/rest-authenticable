# Copyright 2020 Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import logging
from datetime import datetime, timedelta

import passlib

from odoo import _, api, fields, models
from odoo.exceptions import AccessDenied, UserError

from odoo.addons.auth_signup.models.res_partner import random_token

# please read passlib great documentation
# https://passlib.readthedocs.io
# https://passlib.readthedocs.io/en/stable/narr/quickstart.html#choosing-a-hash
# be carefull odoo requirements use an old version of passlib
DEFAULT_CRYPT_CONTEXT = passlib.context.CryptContext(["pbkdf2_sha512"])
DEFAULT_CRYPT_CONTEXT_TOKEN = passlib.context.CryptContext(
    ["pbkdf2_sha512"], pbkdf2_sha512__salt_size=0
)


_logger = logging.getLogger(__name__)


class PartnerAuth(models.Model):
    _name = "partner.auth"
    _description = "Partner Auth"

    partner_id = fields.Many2one("res.partner", "Partner", required=True)
    directory_id = fields.Many2one("directory.auth", "Directory", required=True)
    login = fields.Char(compute="_compute_login", store=True, required=True)
    password = fields.Char(compute="_compute_password", inverse="_inverse_password")
    encrypted_password = fields.Char()
    token_set_password_encrypted = fields.Char()
    token_expiration = fields.Datetime()

    _sql_constraints = [
        (
            "directory_login_uniq",
            "unique (directory_id, login)",
            "Login must be uniq per directory !",
        ),
    ]

    # hack to solve sql constraint
    def _add_login_for_create(self, data):
        partner = self.env["res.partner"].browse(data["partner_id"])
        data["login"] = partner.email

    @api.model_create_multi
    def create(self, data_list):
        for data in data_list:
            self._add_login_for_create(data)
        return super().create(data_list)

    @api.depends("partner_id.email")
    def _compute_login(self):
        for record in self:
            record.login = record.partner_id.email

    def _crypt_context(self):
        return DEFAULT_CRYPT_CONTEXT

    def _check_no_empty(self, login, password):
        # double check by security but calling this through a service should
        # already have check this
        if not (
            isinstance(password, str) and password and isinstance(login, str) and login
        ):
            _logger.warning("Invalid login/password for sign in")
            raise AccessDenied()

    def _get_hashed_password(self, directory, login):
        self.env.cr.execute(
            """
            SELECT id, COALESCE(encrypted_password, '')
            FROM partner_auth
            WHERE login=%s AND directory_id=%s""",
            (login, directory.id),
        )
        hashed = self.env.cr.fetchone()
        if hashed:
            return hashed
        else:
            raise AccessDenied()

    def _compute_password(self):
        for record in self:
            record.password = ""

    def _inverse_password(self):
        # TODO add check on group
        for record in self:
            ctx = record._crypt_context()
            record.encrypted_password = ctx.encrypt(record.password)

    @api.model
    def sign_in(self, directory, login, password):
        self._check_no_empty(login, password)
        _id, hashed = self._get_hashed_password(directory, login)
        valid, replacement = self._crypt_context().verify_and_update(password, hashed)

        if replacement is not None:
            self.browse(_id).encrypted_password = replacement

        if not valid:
            raise AccessDenied()
        return self.browse(_id)

    def _get_template_forgot_password(self, directory):
        return directory.forget_password_template_id

    def _get_template_invite_set_password(self, directory):
        return directory.invite_set_password_template_id

    def _generate_token(self):
        token = random_token()
        self.write(
            {
                "token_set_password_encrypted": self._encrypt_token(token),
                "token_expiration": datetime.now()
                + timedelta(minutes=self.directory_id.set_password_token_duration),
            }
        )
        return token

    def _encrypt_token(self, token):
        return DEFAULT_CRYPT_CONTEXT_TOKEN.hash(token)

    def set_password(self, directory, token_set_password, password):
        hashed_token = self._encrypt_token(token_set_password)
        partner_auth = self.env["partner.auth"].search(
            [
                ("token_set_password_encrypted", "=", hashed_token),
                ("directory_id", "=", directory.id),
            ]
        )
        if partner_auth and partner_auth.token_expiration > datetime.now():
            partner_auth.write(
                {
                    "password": password,
                    "token_set_password_encrypted": False,
                    "token_expiration": False,
                }
            )
            return partner_auth
        else:
            raise UserError(_("The token is not valid, please request a new one"))

    def forgot_password(self, directory, login):
        # forgot_password is called from a job so we return the result as a string
        auth = self.search(
            [
                ("directory_id", "=", directory.id),
                ("login", "=", login),
            ]
        )
        if auth:
            template = self._get_template_forgot_password(directory)
            if not template:
                raise UserError(
                    _("Forgotten Password template is missing for directory {}").format(
                        directory.name
                    )
                )
            token = auth._generate_token()
            template.sudo().with_context(token=token).send_mail(auth.id)
            return "Partner Auth reset password token sent"
        else:
            return "No Partner Auth found, skip"

    def send_invite(self):
        """Use to send an invitation to the user to set
        his password for the first time"""
        self.ensure_one()
        template = self._get_template_invite_set_password(self.directory_id)
        if not template:
            raise UserError(
                _(
                    "Invitation to Set Password template is missing for directory {}"
                ).format(self.directory_id.name)
            )
        token = self._generate_token()
        template.with_context(token=token).send_mail(self.id)
        return True

# Copyright 2020 Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import logging

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class PartnerAuth(models.Model):
    _inherit = "partner.auth"

    # Complexity, rotation

    def _check_password_complexity(self, password):
        self.directory_id.check_password_complexity(password)

    def _check_password_rotation(self, password):
        for past_hash in self.past_hashes:
            if self._crypt_context().verify(password, past_hash):
                raise ValidationError(
                    _("You may not use a password that you have used before.")
                )

    def _prepare_encrypted_password(self, password):
        self._check_password_complexity(password)
        self._check_password_rotation(password)
        result = super()._prepare_encrypted_password(password)
        return result

    def _add_hash_to_history(self):
        rotation_len = self.directory_id.policy_password_rotation
        if not rotation_len:
            return
        self.past_hashes += [self.encrypted_password]
        if len(self.past_hashes) > rotation_len:
            self.past_hashes = self.past_hashes[1:]

    past_hashes = fields.Serialized("Past password hashes", default=[])

    # Expiration

    def _check_password_expiration(self):
        self.directory_id.check_password_expiration(self.date_password_updated)

    @api.model
    def sign_in(self, directory, login, password):
        result = super().sign_in(directory, login, password)
        result._check_password_expiration()
        return result

    def write(self, vals):
        if "encrypted_password" in vals.keys():
            for rec in self:
                rec._add_hash_to_history()
            vals["date_password_updated"] = str(fields.Date.today())
        return super().write(vals)

    date_password_updated = fields.Date(default=lambda x: fields.Date.today())

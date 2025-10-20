# Copyright 2020 Akretion
# Copyright 2020 Odoo SA (some code have been inspired from res_users code)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import re

import zxcvbn

from odoo import _, fields, models
from odoo.exceptions import ValidationError

zxcvbn.feedback._ = _


class DirectoryAuth(models.Model):
    _inherit = "directory.auth"

    policy_password_complexity_lower = fields.Integer("Lowercase characters")
    policy_password_complexity_upper = fields.Integer("Uppercase characters")
    policy_password_complexity_numeric = fields.Integer("Numeric characters")
    policy_password_complexity_special = fields.Integer("Special characters")
    policy_password_complexity_length = fields.Integer("Total length in characters")
    policy_password_complexity_estimate = fields.Integer(
        "Complexity score", help="Calculated using zxcvbn"
    )
    policy_password_rotation = fields.Integer(
        "Passwords kept in history for password comparison"
    )
    policy_password_expiration = fields.Integer(
        "Days before password change is required"
    )

    def _build_error_message(self):
        self.ensure_one()
        message = []
        if self.policy_password_complexity_lower:
            message.append(
                "\n* "
                + "Lowercase letter (At least "
                + str(self.policy_password_complexity_lower)
                + " character)"
            )
        if self.policy_password_complexity_upper:
            message.append(
                "\n* "
                + "Uppercase letter (At least "
                + str(self.policy_password_complexity_upper)
                + " character)"
            )
        if self.policy_password_complexity_numeric:
            message.append(
                "\n* "
                + "Numeric digit (At least "
                + str(self.policy_password_complexity_numeric)
                + " character)"
            )
        if self.policy_password_complexity_special:
            message.append(
                "\n* "
                + "Special character (At least "
                + str(self.policy_password_complexity_special)
                + " character)"
            )
        if message:
            message = [_("Must contain the following:")] + message
        if self.policy_password_complexity_length:
            message = [
                "Password must be %d characters or more."
                % self.policy_password_complexity_length
            ] + message
        return "\r".join(message)

    def check_password_complexity(self, password):
        self.ensure_one()
        if not password:
            return True
        password_regex = [
            "^",
            "(?=.*?[a-z]){" + str(self.policy_password_complexity_lower) + ",}",
            "(?=.*?[A-Z]){" + str(self.policy_password_complexity_upper) + ",}",
            "(?=.*?\\d){" + str(self.policy_password_complexity_numeric) + ",}",
            r"(?=.*?[\W_]){" + str(self.policy_password_complexity_special) + ",}",
            ".{%d,}$" % int(self.policy_password_complexity_length),
        ]
        if not re.search("".join(password_regex), password):
            message = (
                "Password does not pass complexity test:\r"
                + self._build_error_message()
            )
            raise ValidationError(_("%s" % message))

        estimation = zxcvbn.zxcvbn(password)
        if estimation["score"] < self.policy_password_complexity_estimate:
            raise ValidationError(_("Password does not pass complexity score"))

        return True

    def check_password_expiration(self, date_last_changed):
        if (
            self.policy_password_expiration
            and (fields.Date.today() - date_last_changed).days
            > self.policy_password_expiration
        ):
            raise ValidationError(_("Password is expired, please reset it"))

from password_strength import PasswordPolicy
from odoo.exceptions import ValidationError
from odoo import _


def check_password_strength(password):
    policy = PasswordPolicy.from_names(
        length=12, uppercase=1, numbers=1, special=1, nonletters=1,
    )
    if policy.test(password):
        raise ValidationError(_("Password doesn't fit the requirements"))

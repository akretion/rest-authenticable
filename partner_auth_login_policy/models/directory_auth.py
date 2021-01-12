# Copyright 2020 Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import fields, models


class DirectoryAuth(models.Model):
    _inherit = "directory.auth"

    policy_login_attempts = fields.Integer("Maximum login attempts")

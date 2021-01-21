# Copyright 2020 Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class DirectoryAuth(models.Model):
    _inherit = "directory.auth"

    jwt_secret_key = fields.Char()
    jwt_duration = fields.Integer(default=60)

    @property
    def _server_env_fields(self):
        return {"jwt_secret_key": {}}

# Copyright 2020 Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models, fields


class ShopinvaderTenant(models.Model):
    _name = "shopinvader.partner"
    _inherit = ["shopinvader.partner", "tenant.jwt"]

    _tenant_login = "email"
    _tenant_pwd_hash = "password_hash"
    _tenant_identifier = "email"

    password_hash = fields.Char()

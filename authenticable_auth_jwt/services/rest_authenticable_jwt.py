# Copyright 2020 Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.addons.component.core import AbstractComponent


class RestAuthenticableBase(AbstractComponent):
    _name = "rest.authenticable.jwt"
    _inherit = "rest.authenticable.base"
    _usage = "auth"

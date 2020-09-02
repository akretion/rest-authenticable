# Copyright 2020 Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.addons.component.core import AbstractComponent


class RestTenantBase(AbstractComponent):
    _name = "rest.tenant.jwt"
    _inherit = "rest.tenant.base"
    _usage = "auth"

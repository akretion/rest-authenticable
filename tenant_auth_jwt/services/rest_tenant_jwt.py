# Copyright 2020 Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import jwt
import json
from odoo.addons.component.core import AbstractComponent
from odoo.exceptions import ValidationError
from odoo import _
from ..common import get_jwt_token_from_header


class RestTenantBase(AbstractComponent):
    _name = "rest.tenant.jwt"
    _inherit = "rest.tenant.base"
    _usage = "auth"

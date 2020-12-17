#  Copyright (c) Akretion 2020
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo.fields import _
from odoo.addons.datamodel import fields
from odoo.addons.datamodel.core import Datamodel
from marshmallow_objects import validates_schema
from marshmallow.exceptions import ValidationError


class ShopinvaderTenantSignupInput(Datamodel):
    _inherit = ["tenant.signup.input"]
    _name = "shopinvader.tenant.signup.input"

    # Partner fields
    address = fields.NestedModel("tenant.address.base")

    # Binding fields
    external_id = fields.Str()
    sync_date = fields.Date()


class ShopinvaderTenantSignupOutput(Datamodel):
    _inherit = "tenant.signup.output"
    _name = "shopinvader.tenant.signup.output"

#  Copyright (c) Akretion 2020
#  License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)
from odoo.addons.base_rest.controllers.main import RestController


class ShopinvaderTenantJwt(RestController):
    _root_path = "/shopinvader-partner/"
    _collection_name = "shopinvader.backend"
    _default_auth = "public"

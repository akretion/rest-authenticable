# Copyright 2020 Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.addons.base_rest import restapi
from odoo.addons.component.core import Component
from odoo.addons.tenant_auth_jwt.common import jwt_info


class TenantShopinvaderPartner(Component):
    _inherit = "rest.tenant.jwt"
    _name = "shopinvader.tenant.service"
    _usage = "auth"
    _collection = "shopinvader.backend"  # Note this is never used, because the info is contained in the token or route params
    _apply_on = "shopinvader.partner"
    _description = """
    """

    @restapi.method(
        [(["/sign_in"], "POST")],
        input_param=restapi.Datamodel("shopinvader.tenant.signin.input"),
        output_param=restapi.Datamodel("shopinvader.tenant.signin.output"),
        auth="public",
    )
    def sign_in(self, payload):
        result = {"token": self._sign_in(payload)}
        return self.env.datamodels["shopinvader.tenant.signin.output"].load(result)

    @restapi.method(
        [(["/sign_up"], "POST")],
        input_param=restapi.Datamodel("shopinvader.tenant.signup.input"),
        output_param=restapi.Datamodel("shopinvader.tenant.signup.output"),
        auth="public",
    )
    def sign_up(self, payload):
        result = {"result": self._sign_up(payload)}
        return self.env.datamodels["shopinvader.tenant.signup.output"].load(result)

    @restapi.method(
        [(["/sign_out"], "POST")],
        output_param=restapi.Datamodel("shopinvader.tenant.signout.output"),
        auth="jwt",
    )
    def sign_out(self):
        backend, tenant = jwt_info()
        result = {"result": self._sign_out(backend, tenant)}
        return self.env.datamodels["shopinvader.tenant.signout.output"].load(result)

    @restapi.method(
        [(["/reset_password"], "POST")],
        output_param=restapi.Datamodel("shopinvader.tenant.reset.pwd.output"),
        auth="jwt",
    )
    def reset_password(self):
        backend, tenant = jwt_info()
        result = {"result": self._reset_password(backend, tenant)}
        return self.env.datamodels["shopinvader.tenant.reset.pwd.output"].load(result)

    @restapi.method(
        [(["/change_password"], "POST")],
        input_param=restapi.Datamodel("shopinvader.tenant.reset.pwd.input"),
        output_param=restapi.Datamodel("shopinvader.tenant.reset.pwd.output"),
        auth="jwt",
    )
    def change_password(self, payload):
        backend, tenant = jwt_info()
        result = {"result": self._change_password(payload, backend, tenant)}
        return self.env.datamodels["shopinvader.tenant.reset.pwd.output"].load(result)

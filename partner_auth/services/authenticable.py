# Copyright 2020 Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.exceptions import AccessDenied
from odoo.http import request

from odoo.addons.base_rest import restapi
from odoo.addons.base_rest_datamodel.restapi import Datamodel
from odoo.addons.base_rest.http import wrapJsonException
from odoo.addons.component.core import AbstractComponent


class BaseAuthenticable(AbstractComponent):
    _inherit = "base.rest.service"
    _name = "base.authenticable"
    _usage = "auth"

    def _get_directory(self):
        raise NotImplementedError()

    def sign_up(self, payload):
        return (
            self.env[payload.backend.backend_name]
            .browse(payload.backend.backend_id)
            .sign_up(payload)
        )

    @restapi.method(
        [(["/sign_in"], "POST")],
        input_param=Datamodel("authenticable.signin.input"),
        auth="public",
    )
    def sign_in(self, params):
        directory = self._get_directory()
        partner_auth = (
            self.env["partner.auth"]
            .sudo()
            .sign_in(directory, params.login, params.password)
        )
        return self._successfull_sign_in(partner_auth)

    def _invalid_sign_in(self, message):
        return wrapJsonException(AccessDenied(message))

    def _successfull_sign_in(self, partner_auth):
        data = self._prepare_sign_in_data(partner_auth)
        return request.make_json_response(data)

    def _prepare_sign_in_data(self, partner_auth):
        return {"login": partner_auth.login}

    def _sign_out(self):
        return request.make_json_response({})

    @restapi.method(
        [(["/sign_out"], "POST")],
        auth="public",
    )
    def sign_out(self):
        return self._sign_out()

    @restapi.method(
        [(["/set_password"], "POST")],
        input_param=Datamodel("authenticable.set.password.input"),
        auth="public",
    )
    def set_password(self, params):
        directory = self._get_directory()
        partner_auth = (
            self.env["partner.auth"]
            .sudo()
            .set_password(directory, params.token_set_password, params.password)
        )
        return self._successfull_sign_in(partner_auth)

    @restapi.method(
        [(["/forgot_password"], "POST")],
        input_param=Datamodel("authenticable.forget.password.input"),
        auth="public",
    )
    def forgot_password(self, params):
        directory = self._get_directory()
        self.env["partner.auth"].sudo().with_delay().forgot_password(
            directory, params.login
        )
        return {}

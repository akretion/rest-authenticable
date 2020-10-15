# Copyright 2020 Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.addons.component.core import AbstractComponent
from odoo.addons.base_rest import restapi


class BaseAuthenticable(AbstractComponent):
    _inherit = "base.rest.service"
    _name = "base.authenticable"
    _usage = "auth"

    def _find_backend_from_request(self):
        raise NotImplementedError()

    def sign_up(self, payload):
        return (
            self.env[payload.backend.backend_name]
            .browse(payload.backend.backend_id)
            .sign_up(payload)
        )

    @restapi.method(
        [(["/sign_in"], "POST")],
        input_param=restapi.Datamodel("authenticable.signin.input"),
        output_param=restapi.Datamodel("authenticable.signin.output"),
        auth="public",
    )
    def sign_in(self, params):
        backend = self.env[self._collection].sudo().search([
            ("tech_name", "=", params.backend)
            ])
        if backend._sign_in(login=params.login, password=params.password):
            return self._successfull_sign_in()
        else:
            return self._invalid_sign_in()

    def _invalid_sign_in(self):
        raise AccessError("Invalid Login or Password")

    def _successfull_sign_in(self):
        """Each specific implementation should return the right think here
            like a session or a token"""
        return NotImplementedError

    def _sign_out(self, backend, authenticable):
        return backend.sign_out(authenticable)

    def _change_password(self, payload, backend, authenticable):
        return backend.change_password(payload, authenticable)

    def _reset_password(self, payload):
        return (
            self.env[payload.backend.backend_name]
            .browse(payload.backend.backend_id)
            .reset_password(payload.authenticable_identifier)
        )

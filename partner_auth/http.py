from odoo.exceptions import AccessDenied
from odoo.http import HttpRequest
from odoo.loglevels import ustr

from odoo.addons.base_rest.http import wrapJsonException

from .exceptions import InvalidLoginExc


class HttpRestRequest(HttpRequest):
    def _handle_invalid_login_exc(self, e):
        return wrapJsonException(AccessDenied(ustr(e.message)))

    def _handle_exception(self, exception):
        try:
            super()._handle_exception(exception)
        except InvalidLoginExc as e:
            return self._handle_invalid_login_exc(e)

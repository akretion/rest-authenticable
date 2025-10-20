from odoo.exceptions import AccessDenied
from odoo.http import HttpRequest
from odoo.loglevels import ustr

from odoo.addons.base_rest.http import wrapJsonException

from .exceptions import AccountBlockedExc, TooManyAuthExc


class HttpRestRequest(HttpRequest):
    def _handle_invalid_login_exc(self, e):
        e.partner_auth.login_attempts += 1
        return super()._handle_exception(e)

    def _handle_exception(self, exception):
        try:
            super()._handle_exception(exception)
        except (AccountBlockedExc, TooManyAuthExc) as e:
            return wrapJsonException(AccessDenied(ustr(e)))

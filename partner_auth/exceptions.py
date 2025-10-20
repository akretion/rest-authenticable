# Copyright 2021 Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


class InvalidLoginExc(Exception):
    def __init__(self, partner_auth=None, message=None):
        super().__init__(partner_auth)
        self.partner_auth = partner_auth
        self.message = message

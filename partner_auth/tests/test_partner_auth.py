# Copyright 2020 Akretion France (http://www.akretion.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import SavepointCase
from odoo.addons.partner_auth.models.partner_auth import DEFAULT_CRYPT_CONTEXT


class TestPartnerAuth(SavepointCase):

    def setUp(self):
        super().setUp()
        self.directory = self.env.ref("partner_auth.demo_directory")
        self.partner = self.env.ref("partner_auth.demo_readymat_auth")

    def test_encryption(self):
        self.partner.password = "my_pwd"
        self.partner._crypt_context().verify("my_pwd", self.partner.encrypted_password)

    def test_sign_in(self):
        self.partner.password = "my_pwd"
        self.env["partner.auth"].sign_in(self.directory, "ready.mat28@example.com", "my_pwd")
# Copyright 2020 Akretion France (http://www.akretion.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.exceptions import AccessDenied
from odoo.tests.common import SavepointCase

from ..models.partner_auth import AccountBlockedExc, TooManyLoginsExc


class TestPartnerAuthLoginPolicy(SavepointCase):
    def setUp(self):
        super().setUp()
        self.directory = self.env.ref("partner_auth.demo_directory")
        self.partner = self.env.ref("partner_auth.demo_readymat_auth")
        self.partner.password = "covfefe"
        self.directory.policy_login_attempts = 7
        self.partner.login_attempts = 0
        self.env.registry.enter_test_mode(self.env.cr)

    def test_login_counter_incremented(self):
        with self.assertRaises(AccessDenied):
            self.env["partner.auth"].sign_in(
                self.directory, "ready.mat28@example.com", "bad_pwd"
            )
        self.assertEqual(self.partner.login_attempts, 1)

    def test_too_many_logins(self):
        for _x in range(6):
            with self.assertRaises(AccessDenied):
                self.env["partner.auth"].sign_in(
                    self.directory, "ready.mat28@example.com", "wrong_pwd"
                )
        with self.assertRaises(TooManyLoginsExc):
            self.env["partner.auth"].sign_in(
                self.directory, "ready.mat28@example.com", "wrong_pwd"
            )
        with self.assertRaises(AccountBlockedExc):
            self.env["partner.auth"].sign_in(
                self.directory, "ready.mat28@example.com", "wrong_pwd"
            )

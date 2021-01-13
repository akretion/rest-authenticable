# Copyright 2020 Akretion France (http://www.akretion.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api
from odoo.tests.common import TransactionCase
from odoo.exceptions import AccessDenied
from odoo.addons.partner_auth_login_policy.models.partner_auth import (
    TooManyLoginsExc,
    AccountBlockedExc,
)
from mock import Mock


class TestPartnerAuthLoginPolicy(TransactionCase):
    def setUp(self):
        super().setUp()
        self.directory = self.env.ref("partner_auth.demo_directory")
        self.partner = self.env.ref("partner_auth.demo_readymat_auth")
        self.partner.password = "covfefe"
        self.directory.policy_login_attempts = 7
        self.partner.login_attempts = 0

    def test_login_counter_incremented(self):
        with self.assertRaises(AccessDenied):
            self.env["partner.auth"].sign_in(self.directory, "ready.mat28@example.com", "bad_pwd")
        self.assertEqual(self.partner.login_attempts, 1)

    def test_too_many_logins(self):
        for x in range(6):
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
